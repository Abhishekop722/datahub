import datahub.emitter.mce_builder as builder
from datahub.emitter.mcp import MetadataChangeProposalWrapper
from datahub.emitter.rest_emitter import DatahubRestEmitter
from datahub.metadata.schema_classes import DatasetPropertiesClass


dataset_properties = DatasetPropertiesClass(description="This table stored the canonical User profile",
    customProperties={
         "governance": "ENABLED"
    })
metadata_event = MetadataChangeProposalWrapper(
    entityUrn=builder.make_dataset_urn("hive", "dataset_1"),
    aspect=dataset_properties,
)
metadata_event2 = MetadataChangeProposalWrapper(
    entityUrn=builder.make_dataset_urn("hive", "dataset_2"),
    aspect=dataset_properties,
)
metadata_event3 = MetadataChangeProposalWrapper(
    entityUrn=builder.make_dataset_urn("hive", "dataset_3"),
    aspect=dataset_properties,
)

# Construct a lineage object.
lineage_mce = builder.make_lineage_mce(
    [
        builder.make_dataset_urn("hive", "dataset_2"),  # Upstream
        builder.make_dataset_urn("hive", "dataset_3"),  # Upstream
    ],
    builder.make_dataset_urn("hive", "dataset_1"),  # Downstream
)

# Create an emitter to the GMS REST API.
emitter = DatahubRestEmitter("http://127.0.0.1:50440", token="eyJhbGciOiJIUzI1NiJ9.eyJhY3RvclR5cGUiOiJVU0VSIiwiYWN0b3JJZCI6ImRhdGFodWIiLCJ0eXBlIjoiUEVSU09OQUwiLCJ2ZXJzaW9uIjoiMiIsImp0aSI6Ijk1ZDAzNDk5LTg0YjYtNDFiMC05NDMwLThkMzVjMWJmYmVmYyIsInN1YiI6ImRhdGFodWIiLCJleHAiOjE3MDk4ODczMTgsImlzcyI6ImRhdGFodWItbWV0YWRhdGEtc2VydmljZSJ9.PAk14CkZuUxc__JBC4yu_xOz9OfTRmDSHl4euIOzjac")

# Emit metadata!
try:
    emitter.emit(metadata_event)
    emitter.emit(metadata_event2)
    emitter.emit(metadata_event3)
    emitter.emit_mce(lineage_mce)
    print("Successfully wrote to DataHub")
except Exception as e:
    print("Failed to write to DataHub")
    raise e
