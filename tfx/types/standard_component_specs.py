# Lint as: python2, python3
# Copyright 2019 Google LLC. All Rights Reserved.
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
"""Component specifications for the standard set of TFX Components."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from typing import List, Text

import tensorflow_model_analysis as tfma
from tfx.proto import bulk_inferrer_pb2
from tfx.proto import evaluator_pb2
from tfx.proto import example_gen_pb2
from tfx.proto import infra_validator_pb2
from tfx.proto import pusher_pb2
from tfx.proto import range_config_pb2
from tfx.proto import trainer_pb2
from tfx.proto import transform_pb2
from tfx.proto import tuner_pb2
from tfx.types import standard_artifacts
from tfx.types.component_spec import ChannelParameter
from tfx.types.component_spec import ComponentSpec
from tfx.types.component_spec import ExecutionParameter

# Parameters keys for modules
# Shared Keys across components
SCHEMA_KEY = 'schema'
EXAMPLES_KEY = 'examples'
MODEL_KEY = 'model'
BLESSING_KEY = 'blessing'
MODULE_FILE_KEY = 'module_file'
# Key for example_validator
EXCLUDE_SPLITS_KEY = 'exclude_splits'
STATISTICS_KEY = 'statistics'
ANOMALIES_KEY = 'anomalies'
# Key for evaluator
EVAL_CONFIG_KEY = 'eval_config'
FEATURE_SLICING_SPEC_KEY = 'feature_slicing_spec'
FAIRNESS_INDICATOR_THRESHOLDS_KEY = 'fairness_indicator_thresholds'
EXAMPLE_SPLITS_KEY = 'example_splits'
MODULE_PATH_KEY = 'module_path'
BASELINE_MODEL_KEY = 'baseline_model'
EVALUATION_KEY = 'evaluation'
# Key for for infra_validator
SERVING_SPEC_KEY = 'serving_spec'
VALIDATION_SPEC_KEY = 'validation_spec'
REQUEST_SPEC_KEY = 'request_spec'
# Key for TrainerSpec
TRAIN_ARGS_KEY = 'train_args'
EVAL_ARGS_KEY = 'eval_args'
RUN_FN_KEY = 'run_fn'
TRAINER_FN_KEY = 'trainer_fn'
CUSTOM_CONFIG_KEY = 'custom_config'
TRANSFORM_GRAPH_KEY = 'transform_graph'
BASE_MODEL_KEY = 'base_model'
HYPERPARAMETERS_KEY = 'hyperparameters'
MODEL_RUN_KEY = 'model_run'


class BulkInferrerSpec(ComponentSpec):
  """BulkInferrer component spec."""

  PARAMETERS = {
      'model_spec':
          ExecutionParameter(type=bulk_inferrer_pb2.ModelSpec, optional=True),
      'data_spec':
          ExecutionParameter(type=bulk_inferrer_pb2.DataSpec, optional=True),
      'output_example_spec':
          ExecutionParameter(
              type=bulk_inferrer_pb2.OutputExampleSpec, optional=True),
  }
  INPUTS = {
      'examples':
          ChannelParameter(type=standard_artifacts.Examples),
      'model':
          ChannelParameter(type=standard_artifacts.Model, optional=True),
      'model_blessing':
          ChannelParameter(
              type=standard_artifacts.ModelBlessing, optional=True),
  }
  OUTPUTS = {
      'inference_result':
          ChannelParameter(
              type=standard_artifacts.InferenceResult, optional=True),
      'output_examples':
          ChannelParameter(type=standard_artifacts.Examples, optional=True),
  }


class EvaluatorSpec(ComponentSpec):
  """Evaluator component spec."""

  PARAMETERS = {
      EVAL_CONFIG_KEY:
          ExecutionParameter(type=tfma.EvalConfig, optional=True),
      # TODO(mdreves): Deprecated, use eval_config.slicing_specs.
      FEATURE_SLICING_SPEC_KEY:
          ExecutionParameter(
              type=evaluator_pb2.FeatureSlicingSpec, optional=True),
      # This parameter is experimental: its interface and functionality may
      # change at any time.
      FAIRNESS_INDICATOR_THRESHOLDS_KEY:
          ExecutionParameter(type=List[float], optional=True),
      EXAMPLE_SPLITS_KEY:
          ExecutionParameter(type=(str, Text), optional=True),
      MODULE_FILE_KEY:
          ExecutionParameter(type=(str, Text), optional=True),
      MODULE_PATH_KEY:
          ExecutionParameter(type=(str, Text), optional=True),
  }
  INPUTS = {
      EXAMPLES_KEY:
          ChannelParameter(type=standard_artifacts.Examples),
      MODEL_KEY:
          ChannelParameter(type=standard_artifacts.Model),
      BASELINE_MODEL_KEY:
          ChannelParameter(type=standard_artifacts.Model, optional=True),
      SCHEMA_KEY:
          ChannelParameter(type=standard_artifacts.Schema, optional=True),
  }
  OUTPUTS = {
      EVALUATION_KEY: ChannelParameter(type=standard_artifacts.ModelEvaluation),
      BLESSING_KEY: ChannelParameter(type=standard_artifacts.ModelBlessing),
  }


class ExampleValidatorSpec(ComponentSpec):
  """ExampleValidator component spec."""

  PARAMETERS = {
      EXCLUDE_SPLITS_KEY: ExecutionParameter(type=(str, Text), optional=True),
  }
  INPUTS = {
      STATISTICS_KEY:
          ChannelParameter(type=standard_artifacts.ExampleStatistics),
      SCHEMA_KEY:
          ChannelParameter(type=standard_artifacts.Schema),
  }
  OUTPUTS = {
      ANOMALIES_KEY: ChannelParameter(type=standard_artifacts.ExampleAnomalies),
  }


class FileBasedExampleGenSpec(ComponentSpec):
  """File-based ExampleGen component spec."""

  PARAMETERS = {
      'input_base':
          ExecutionParameter(type=(str, Text)),
      'input_config':
          ExecutionParameter(type=example_gen_pb2.Input),
      'output_config':
          ExecutionParameter(type=example_gen_pb2.Output),
      'output_data_format':
          ExecutionParameter(type=int),  # example_gen_pb2.PayloadType enum.
      'custom_config':
          ExecutionParameter(type=example_gen_pb2.CustomConfig, optional=True),
      'range_config':
          ExecutionParameter(type=range_config_pb2.RangeConfig, optional=True),
  }
  INPUTS = {}
  OUTPUTS = {
      'examples': ChannelParameter(type=standard_artifacts.Examples),
  }


class QueryBasedExampleGenSpec(ComponentSpec):
  """Query-based ExampleGen component spec."""

  PARAMETERS = {
      'input_config':
          ExecutionParameter(type=example_gen_pb2.Input),
      'output_config':
          ExecutionParameter(type=example_gen_pb2.Output),
      'output_data_format':
          ExecutionParameter(type=int),  # example_gen_pb2.PayloadType enum.
      'custom_config':
          ExecutionParameter(type=example_gen_pb2.CustomConfig, optional=True),
  }
  INPUTS = {}
  OUTPUTS = {
      'examples': ChannelParameter(type=standard_artifacts.Examples),
  }


class InfraValidatorSpec(ComponentSpec):
  """InfraValidator component spec."""

  PARAMETERS = {
      SERVING_SPEC_KEY:
          ExecutionParameter(type=infra_validator_pb2.ServingSpec),
      VALIDATION_SPEC_KEY:
          ExecutionParameter(
              type=infra_validator_pb2.ValidationSpec, optional=True),
      REQUEST_SPEC_KEY:
          ExecutionParameter(
              type=infra_validator_pb2.RequestSpec, optional=True)
  }

  INPUTS = {
      MODEL_KEY:
          ChannelParameter(type=standard_artifacts.Model),
      EXAMPLES_KEY:
          ChannelParameter(type=standard_artifacts.Examples, optional=True),
  }

  OUTPUTS = {
      BLESSING_KEY: ChannelParameter(type=standard_artifacts.InfraBlessing),
  }


class ModelValidatorSpec(ComponentSpec):
  """ModelValidator component spec."""

  PARAMETERS = {}
  INPUTS = {
      'examples': ChannelParameter(type=standard_artifacts.Examples),
      'model': ChannelParameter(type=standard_artifacts.Model),
  }
  OUTPUTS = {
      'blessing': ChannelParameter(type=standard_artifacts.ModelBlessing),
  }


class PusherSpec(ComponentSpec):
  """Pusher component spec."""

  PARAMETERS = {
      'push_destination':
          ExecutionParameter(type=pusher_pb2.PushDestination, optional=True),
      'custom_config':
          ExecutionParameter(type=(str, Text), optional=True),
  }
  INPUTS = {
      'model':
          ChannelParameter(type=standard_artifacts.Model),
      'model_blessing':
          ChannelParameter(
              type=standard_artifacts.ModelBlessing, optional=True),
      'infra_blessing':
          ChannelParameter(
              type=standard_artifacts.InfraBlessing, optional=True),
  }
  OUTPUTS = {
      'pushed_model': ChannelParameter(type=standard_artifacts.PushedModel),
  }
  # TODO(b/139281215): these input / output names have recently been renamed.
  # These compatibility aliases are temporarily provided for backwards
  # compatibility.
  _INPUT_COMPATIBILITY_ALIASES = {
      'model_export': 'model',
  }
  _OUTPUT_COMPATIBILITY_ALIASES = {
      'model_push': 'pushed_model',
  }


class SchemaGenSpec(ComponentSpec):
  """SchemaGen component spec."""

  PARAMETERS = {
      'infer_feature_shape': ExecutionParameter(type=int, optional=True),
      'exclude_splits': ExecutionParameter(type=(str, Text), optional=True),
  }
  INPUTS = {
      'statistics': ChannelParameter(type=standard_artifacts.ExampleStatistics),
  }
  OUTPUTS = {
      'schema': ChannelParameter(type=standard_artifacts.Schema),
  }
  # TODO(b/139281215): these input / output names have recently been renamed.
  # These compatibility aliases are temporarily provided for backwards
  # compatibility.
  _INPUT_COMPATIBILITY_ALIASES = {
      'stats': 'statistics',
  }
  _OUTPUT_COMPATIBILITY_ALIASES = {
      'output': 'schema',
  }


class StatisticsGenSpec(ComponentSpec):
  """StatisticsGen component spec."""

  PARAMETERS = {
      'stats_options_json': ExecutionParameter(type=(str, Text), optional=True),
      'exclude_splits': ExecutionParameter(type=(str, Text), optional=True),
  }
  INPUTS = {
      'examples': ChannelParameter(type=standard_artifacts.Examples),
      'schema': ChannelParameter(type=standard_artifacts.Schema, optional=True),
  }
  OUTPUTS = {
      'statistics': ChannelParameter(type=standard_artifacts.ExampleStatistics),
  }
  # TODO(b/139281215): these input / output names have recently been renamed.
  # These compatibility aliases are temporarily provided for backwards
  # compatibility.
  _INPUT_COMPATIBILITY_ALIASES = {
      'input_data': 'examples',
  }
  _OUTPUT_COMPATIBILITY_ALIASES = {
      'output': 'statistics',
  }


class TrainerSpec(ComponentSpec):
  """Trainer component spec."""

  PARAMETERS = {
      TRAIN_ARGS_KEY: ExecutionParameter(type=trainer_pb2.TrainArgs),
      EVAL_ARGS_KEY: ExecutionParameter(type=trainer_pb2.EvalArgs),
      MODULE_FILE_KEY: ExecutionParameter(type=(str, Text), optional=True),
      RUN_FN_KEY: ExecutionParameter(type=(str, Text), optional=True),
      TRAINER_FN_KEY: ExecutionParameter(type=(str, Text), optional=True),
      CUSTOM_CONFIG_KEY: ExecutionParameter(type=(str, Text), optional=True),
  }
  INPUTS = {
      EXAMPLES_KEY:
          ChannelParameter(type=standard_artifacts.Examples),
      TRANSFORM_GRAPH_KEY:
          ChannelParameter(
              type=standard_artifacts.TransformGraph, optional=True),
      SCHEMA_KEY:
          ChannelParameter(type=standard_artifacts.Schema, optional=True),
      BASE_MODEL_KEY:
          ChannelParameter(type=standard_artifacts.Model, optional=True),
      HYPERPARAMETERS_KEY:
          ChannelParameter(
              type=standard_artifacts.HyperParameters, optional=True),
  }
  OUTPUTS = {
      MODEL_KEY: ChannelParameter(type=standard_artifacts.Model),
      MODEL_RUN_KEY: ChannelParameter(type=standard_artifacts.ModelRun)
  }


class TunerSpec(ComponentSpec):
  """ComponentSpec for TFX Tuner Component."""

  PARAMETERS = {
      'module_file': ExecutionParameter(type=(str, Text), optional=True),
      'tuner_fn': ExecutionParameter(type=(str, Text), optional=True),
      'train_args': ExecutionParameter(type=trainer_pb2.TrainArgs),
      'eval_args': ExecutionParameter(type=trainer_pb2.EvalArgs),
      'tune_args': ExecutionParameter(type=tuner_pb2.TuneArgs, optional=True),
      'custom_config': ExecutionParameter(type=(str, Text), optional=True),
  }
  INPUTS = {
      'examples':
          ChannelParameter(type=standard_artifacts.Examples),
      'schema':
          ChannelParameter(type=standard_artifacts.Schema, optional=True),
      'transform_graph':
          ChannelParameter(
              type=standard_artifacts.TransformGraph, optional=True),
  }
  OUTPUTS = {
      'best_hyperparameters':
          ChannelParameter(type=standard_artifacts.HyperParameters),
  }


class TransformSpec(ComponentSpec):
  """Transform component spec."""

  PARAMETERS = {
      'module_file':
          ExecutionParameter(type=(str, Text), optional=True),
      'preprocessing_fn':
          ExecutionParameter(type=(str, Text), optional=True),
      'force_tf_compat_v1':
          ExecutionParameter(type=int, optional=True),
      'custom_config':
          ExecutionParameter(type=(str, Text), optional=True),
      'splits_config':
          ExecutionParameter(type=transform_pb2.SplitsConfig, optional=True),
  }
  INPUTS = {
      'examples':
          ChannelParameter(type=standard_artifacts.Examples),
      'schema':
          ChannelParameter(type=standard_artifacts.Schema),
      'analyzer_cache':
          ChannelParameter(
              type=standard_artifacts.TransformCache, optional=True),
  }
  OUTPUTS = {
      'transform_graph':
          ChannelParameter(type=standard_artifacts.TransformGraph),
      'transformed_examples':
          ChannelParameter(type=standard_artifacts.Examples, optional=True),
      'updated_analyzer_cache':
          ChannelParameter(
              type=standard_artifacts.TransformCache, optional=True),
  }
  # TODO(b/139281215): these input / output names have recently been renamed.
  # These compatibility aliases are temporarily provided for backwards
  # compatibility.
  _INPUT_COMPATIBILITY_ALIASES = {
      'input_data': 'examples',
  }
  _OUTPUT_COMPATIBILITY_ALIASES = {
      'transform_output': 'transform_graph',
  }
