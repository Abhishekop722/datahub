import json

from datahub.emitter.rest_emitter import DatahubRestEmitter
from datahub.emitter.mce_builder import make_tag_urn

from datahub.metadata.schema_classes import (
    ChangeTypeClass,
    GenericAspectClass,
    MetadataChangeProposalClass,
    GlobalTagsClass,
    TagAssociationClass
)

tag_to_add = make_tag_urn("DataMesh")
tag_association_to_add = TagAssociationClass(tag=tag_to_add)
tags_aspect_to_set = GlobalTagsClass(tags=[tag_association_to_add])

dq_aspect = {
    "outputPorts": [
        {
            "name": "projects-ADLS",
            "id": "some_unique_system_generated_id",
            "asset": "projects",
            "format": "csv",
            "natureOfDataset": "ACTUAL",
            "intendedPurpose": "MODEL TRAINING",
            "classification": "INTERNAL",
            "status": "ACTIVE",
            "storageAccountName": "pocdevsa",
            "containerName": "gitlab",
            "directoryPath": "projects"
        }
    ]
}

emitter: DatahubRestEmitter = DatahubRestEmitter(gms_server="http://127.0.0.1:50440", token="eyJhbGciOiJIUzI1NiJ9.eyJhY3RvclR5cGUiOiJVU0VSIiwiYWN0b3JJZCI6ImRhdGFodWIiLCJ0eXBlIjoiUEVSU09OQUwiLCJ2ZXJzaW9uIjoiMiIsImp0aSI6Ijk1ZDAzNDk5LTg0YjYtNDFiMC05NDMwLThkMzVjMWJmYmVmYyIsInN1YiI6ImRhdGFodWIiLCJleHAiOjE3MDk4ODczMTgsImlzcyI6ImRhdGFodWItbWV0YWRhdGEtc2VydmljZSJ9.PAk14CkZuUxc__JBC4yu_xOz9OfTRmDSHl4euIOzjac")

dataset_urn = "urn:li:dataProduct:617906a6-4126-414c-9b7d-495b28c85b62"
mcp_raw: MetadataChangeProposalClass = MetadataChangeProposalClass(
    entityType="dataProduct",
    entityUrn=dataset_urn,
    changeType=ChangeTypeClass.UPSERT,
    aspectName="outputPorts",
    aspect=GenericAspectClass(
        contentType="application/json",
        value=json.dumps(dq_aspect).encode("utf-8"),

    ),
)

try:
    emitter.emit(mcp_raw)
    print("Successfully wrote to DataHub")
except Exception as e:
    print("Failed to write to DataHub")
    raise e
