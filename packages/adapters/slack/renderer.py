from packages.schemas.dossier import DossierStub, PreVisitDossier

def render_stub(stub: DossierStub) -> list:
    return [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*Company:* {stub.company_facts.get('name', 'Unknown')}\n*Vertical:* {stub.verified_vertical}"
            }
        }
    ]

def render_dossier(dossier: PreVisitDossier) -> list:
    return [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*Dossier for:* {dossier.prospect_id}\n*Taxonomy:* {dossier.process_taxonomy.primary_process}"
            }
        }
    ]
