from packages.schemas.dossier import PreVisitDossier

def render_doc_content(dossier: PreVisitDossier) -> str:
    """
    Schema -> Google Doc structured paragraphs + tables
    """
    content = f"Matta Pre-Visit Dossier — {dossier.prospect_id}\n\n"
    content += f"§1 Process Taxonomy\n{dossier.process_taxonomy.primary_process}\n\n"
    content += "§2 Defect-class hypothesis\n"
    content += f"With {dossier.defect_hypothesis.coverage * 100}% coverage, dominant defect classes are in: {dossier.defect_hypothesis.conformal_set}\n\n"
    content += f"§3 Comparable Matta deployment\n{dossier.comparable_deployment.matta_customer_anchor} - {dossier.comparable_deployment.dimension_of_comparability}\n\n"
    content += "§4 Integration risk register\n"
    for finding in dossier.risk_register.findings:
        content += f"- {finding.category}: {finding.severity} - {finding.note}\n"
    content += "\n§5 Suggested approach\n"
    content += f"{dossier.suggested_approach.template}\n"
    return content
