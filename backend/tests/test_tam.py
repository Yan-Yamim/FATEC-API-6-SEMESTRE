import pytest
from sqlalchemy import text


@pytest.mark.asyncio
async def test_trigger_pipeline_flow_data_integrity(session, mongo_db, triggered_job):
    job_id = str(triggered_job["job_id"])
    original_dist = triggered_job["dist_data"]

    stmt = text("SELECT job_id FROM distribuidoras WHERE id = :id AND date_gdb = :ano")
    db_job_id = (await session.execute(
        stmt, {"id": original_dist["id"], "ano": original_dist["date_gdb"]}
    )).scalar()
    assert str(db_job_id) == job_id

    job_doc = await mongo_db['jobs'].find_one({
        "dist_name": original_dist["dist_name"],
        "ano_gdb": original_dist["date_gdb"]
    }, sort=[("_id", -1)])

    assert job_doc is not None, "Job não encontrado no MongoDB"
    assert str(job_doc['job_id']) == job_id
    assert job_doc['status'] == "started"