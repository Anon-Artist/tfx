# Lint as: python2, python3
# Copyright 2020 Google LLC. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Tests for tfx.components.trainer.executor."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from ml_metadata.proto import metadata_store_pb2
import mock
import os
import tensorflow as tf
from tensorflow.python.lib.io import file_io  # pylint: disable=g-direct-tensorflow-import
from tfx.experimental.pipeline_testing import dummy_component_launcher
from tfx.experimental.pipeline_testing import dummy_executor
from tfx.orchestration import data_types
from tfx.orchestration import metadata
from tfx.orchestration import publisher
from tfx.orchestration.launcher import test_utils
from tfx.types import channel_utils

class DummyLauncherTest(tf.test.TestCase):

  def setUp(self):
    super(DummyLauncherTest, self).setUp()
    test_dir = os.path.join(
        os.environ.get('TEST_UNDECLARED_OUTPUTS_DIR', self.get_temp_dir()),
        self._testMethodName)

    connection_config = metadata_store_pb2.ConnectionConfig()
    connection_config.sqlite.SetInParent()
    self.metadata_connection = metadata.Metadata(connection_config)

    self.pipeline_root = os.path.join(test_dir, 'Test')
    output_path = os.path.join(test_dir, 'output')
    self.record_path = os.path.join(test_dir, 'record')

    input_artifact = test_utils._InputArtifact()  # pylint: disable=protected-access
    output_artifact = test_utils._OutputArtifact()  # pylint: disable=protected-access
    output_artifact.uri = output_path
    self.component = test_utils._FakeComponent(  # pylint: disable=protected-access
        name='FakeComponent',
        input_channel=channel_utils.as_channel([input_artifact]),
        output_channel=channel_utils.as_channel([output_artifact]))
    self.driver_args = data_types.DriverArgs(enable_cache=True)

    self.pipeline_info = data_types.PipelineInfo(
        pipeline_name='Test', pipeline_root=self.pipeline_root, run_id='123')

  @mock.patch.object(publisher, 'Publisher')
  def testCustomDummyExecutor(self, mock_publisher):
    # verify whether custom dummy substitution works
    mock_publisher.return_value.publish_execution.return_value = {}
    tf.io.gfile.makedirs(self.record_path)
    component_ids = []
    component_map = \
        {'_FakeComponent.FakeComponent': dummy_executor.CustomDummyExecutor}

    MyDummyLauncher = \
        dummy_component_launcher.create_dummy_launcher_class(
            self.record_path,
            component_ids,
            component_map)

    launcher = MyDummyLauncher.create(
        component=self.component,
        pipeline_info=self.pipeline_info,
        driver_args=self.driver_args,
        metadata_connection=self.metadata_connection,
        beam_pipeline_args=[],
        additional_pipeline_args={})
    launcher.launch()

    output_path = self.component.outputs['output'].get()[0].uri
    generated_file = os.path.join(output_path, "test.txt")
    self.assertTrue(tf.io.gfile.exists(generated_file))
    contents = file_io.read_file_to_string(generated_file)
    self.assertEqual('custom component', contents)

  @mock.patch.object(publisher, 'Publisher')
  def testDummyExecutor(self, mock_publisher):
    # verify whether dummy substitution works
    mock_publisher.return_value.publish_execution.return_value = {}

    record_file = os.path.join(self.record_path, 'output/recorded.txt')
    tf.io.gfile.makedirs(os.path.dirname(record_file))
    file_io.write_string_to_file(record_file, "hello world")
    print("record_file")

    component_ids = ['_FakeComponent.FakeComponent']
    component_map = {}

    MyDummyLauncher = \
        dummy_component_launcher.create_dummy_launcher_class(self.record_path,
                                                             component_ids,
                                                             component_map)

    launcher = MyDummyLauncher.create(
        component=self.component,
        pipeline_info=self.pipeline_info,
        driver_args=self.driver_args,
        metadata_connection=self.metadata_connection,
        beam_pipeline_args=[],
        additional_pipeline_args={})
    launcher.launch()

    output_path = self.component.outputs['output'].get()[0].uri
    copied_file = os.path.join(output_path, "recorded.txt")
    self.assertTrue(tf.io.gfile.exists(copied_file))
    contents = file_io.read_file_to_string(copied_file)
    self.assertEqual('hello world', contents)

if __name__ == '__main__':
  tf.test.main()
