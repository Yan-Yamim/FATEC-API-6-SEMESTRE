import pytest
from sqlalchemy import select
from types import SimpleNamespace
from unittest.mock import MagicMock

from backend.core.models import Distribuidora


def _mock_all_tasks(monkeypatch, download_task_mock):
    """Mocka o download e as 4 tasks de criticidade/render no pipeline_trigger."""
    monkeypatch.setattr(
        'backend.services.pipeline_trigger.task_download_gdb.delay',
        download_task_mock,
    )
    noop = MagicMock()
    monkeypatch.setattr(
        'backend.services.pipeline_trigger.task_score_criticidade.delay', noop
    )
    monkeypatch.setattr(
        'backend.services.pipeline_trigger.task_mapa_criticidade.delay', noop
    )
    monkeypatch.setattr(
        'backend.services.pipeline_trigger.task_render_tabela_score.delay', noop
    )
    monkeypatch.setattr(
        'backend.services.pipeline_trigger.task_render_mapa_calor.delay', noop
    )
    return noop


@pytest.mark.asyncio
async def test_pipeline_trigger_retorna_202_quando_valido(
    client,
    session,
    monkeypatch,
):
    session.add(
        Distribuidora(
            id='item-123',
            date_gdb=2026,
            dist_name='DIST TESTE',
        )
    )
    await session.commit()

    async def fake_resolve(_distribuidora_id):
        return 'https://www.arcgis.com/sharing/rest/content/items/item-123/data'

    fake_task = SimpleNamespace(id='task-1')
    mock_download_delay = MagicMock(return_value=fake_task)
    _mock_all_tasks(monkeypatch, mock_download_delay)
    monkeypatch.setattr(
        'backend.services.pipeline_trigger.resolve_download_url_from_aneel',
        fake_resolve,
    )

    response = await client.post(
        '/pipeline/trigger',
        json={'distribuidora_id': 'item-123', 'ano': 2026},
    )

    assert response.status_code == 202
    body = response.json()
    assert body['task_id'] == 'task-1'
    assert body['status'] == 'queued'
    assert body['distribuidora_id'] == 'item-123'
    assert body['ano'] == 2026
    assert (
        body['download_url']
        == 'https://www.arcgis.com/sharing/rest/content/items/item-123/data'
    )
    assert 'job_id' in body

    mock_download_delay.assert_called_once()

    persisted = (
        (
            await session.execute(
                select(Distribuidora).where(
                    Distribuidora.id == 'item-123',
                    Distribuidora.date_gdb == 2026,
                )
            )
        )
        .scalars()
        .one()
    )
    assert persisted.job_id == body['job_id']
    assert persisted.processed_at is not None


@pytest.mark.asyncio
async def test_pipeline_trigger_dispara_todas_as_tasks(
    client,
    session,
    monkeypatch,
):
    """Verifica que as 5 tasks (download + criticidade + render) são enfileiradas."""
    session.add(
        Distribuidora(id='item-all-tasks', date_gdb=2026, dist_name='DIST ALL')
    )
    await session.commit()

    async def fake_resolve(_):
        return 'https://www.arcgis.com/sharing/rest/content/items/item-all-tasks/data'

    fake_task = SimpleNamespace(id='t-download')
    mock_download = MagicMock(return_value=fake_task)
    mock_score = MagicMock()
    mock_mapa = MagicMock()
    mock_tabela = MagicMock()
    mock_calor = MagicMock()

    monkeypatch.setattr(
        'backend.services.pipeline_trigger.task_download_gdb.delay', mock_download
    )
    monkeypatch.setattr(
        'backend.services.pipeline_trigger.task_score_criticidade.delay', mock_score
    )
    monkeypatch.setattr(
        'backend.services.pipeline_trigger.task_mapa_criticidade.delay', mock_mapa
    )
    monkeypatch.setattr(
        'backend.services.pipeline_trigger.task_render_tabela_score.delay', mock_tabela
    )
    monkeypatch.setattr(
        'backend.services.pipeline_trigger.task_render_mapa_calor.delay', mock_calor
    )
    monkeypatch.setattr(
        'backend.services.pipeline_trigger.resolve_download_url_from_aneel',
        fake_resolve,
    )

    response = await client.post(
        '/pipeline/trigger',
        json={'distribuidora_id': 'item-all-tasks', 'ano': 2026},
    )

    assert response.status_code == 202
    job_id = response.json()['job_id']

    mock_download.assert_called_once()
    mock_score.assert_called_once_with(job_id, 'DIST ALL', 2026)
    mock_mapa.assert_called_once_with(job_id, 'item-all-tasks', 'DIST ALL', 2026)
    mock_tabela.assert_called_once_with(job_id, 'DIST ALL', 2026)
    mock_calor.assert_called_once_with(job_id, 'DIST ALL', 2026)


@pytest.mark.asyncio
async def test_pipeline_trigger_payload_invalido_retorna_422(client):
    response = await client.post(
        '/pipeline/trigger',
        json={'distribuidora_id': 'item-123', 'ano': 'nao-inteiro'},
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_pipeline_trigger_distribuidora_nao_cadastrada_retorna_404(
    client,
    monkeypatch,
):
    async def fake_resolve(_):
        return 'https://url.fake/data'

    monkeypatch.setattr(
        'backend.services.pipeline_trigger.resolve_download_url_from_aneel',
        fake_resolve,
    )

    response = await client.post(
        '/pipeline/trigger',
        json={'distribuidora_id': 'id-inexistente', 'ano': 2026},
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_pipeline_trigger_ja_acionada_retorna_409(
    client,
    session,
    monkeypatch,
):
    session.add(
        Distribuidora(
            id='item-duplicado',
            date_gdb=2026,
            dist_name='DIST TESTE',
            job_id='job-ja-existente',
        )
    )
    await session.commit()

    async def fake_resolve(_distribuidora_id):
        pytest.fail('Não deveria resolver URL para pipeline já acionada')

    monkeypatch.setattr(
        'backend.services.pipeline_trigger.resolve_download_url_from_aneel',
        fake_resolve,
    )
    monkeypatch.setattr(
        'backend.services.pipeline_trigger.task_download_gdb.delay',
        lambda *a, **kw: pytest.fail('Não deveria enfileirar pipeline já acionada'),
    )

    response = await client.post(
        '/pipeline/trigger',
        json={'distribuidora_id': 'item-duplicado', 'ano': 2026},
    )

    assert response.status_code == 409
    assert (
        response.json()['detail']
        == 'Pipeline já foi acionada para a distribuidora no ano informado'
    )


@pytest.mark.asyncio
async def test_pipeline_trigger_item_inexistente_aneel_retorna_404(
    client,
    session,
    monkeypatch,
):
    session.add(
        Distribuidora(id='item-404', date_gdb=2026, dist_name='DIST TESTE')
    )
    await session.commit()

    async def fake_resolve(_distribuidora_id):
        raise LookupError('Item não encontrado na ANEEL')

    monkeypatch.setattr(
        'backend.services.pipeline_trigger.resolve_download_url_from_aneel',
        fake_resolve,
    )

    response = await client.post(
        '/pipeline/trigger',
        json={'distribuidora_id': 'item-404', 'ano': 2026},
    )

    assert response.status_code == 404
    assert response.json()['detail'] == 'Item não encontrado na ANEEL'


@pytest.mark.asyncio
async def test_pipeline_trigger_aneel_indisponivel_retorna_502(
    client,
    session,
    monkeypatch,
):
    session.add(
        Distribuidora(id='item-502', date_gdb=2026, dist_name='DIST TESTE')
    )
    await session.commit()

    async def fake_resolve(_distribuidora_id):
        raise RuntimeError('ANEEL indisponível no momento')

    monkeypatch.setattr(
        'backend.services.pipeline_trigger.resolve_download_url_from_aneel',
        fake_resolve,
    )

    response = await client.post(
        '/pipeline/trigger',
        json={'distribuidora_id': 'item-502', 'ano': 2026},
    )

    assert response.status_code == 502
    assert response.json()['detail'] == 'ANEEL indisponível no momento'
