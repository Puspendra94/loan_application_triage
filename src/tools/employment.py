"""
Employment Verification Tool

Mock implementation of employment verification service.
"""

from langchain_core.tools import tool


@tool
def mock_employment_verification(employer_name: str) -> dict:
    """
    Mock employment verification tool
    :param employer_name: Name of the employer
    :return: dict with verified (bool), employment_type, years_in_business
    """

    employer_name = employer_name.strip().lower()

    # Known MNCs
    mnc_companies = {"infosys", "tcs", "wipro"}

    if employer_name in mnc_companies:
        return {
            "verified": True,
            "employment_type": "MNC",
            "years_in_business": 30
        }

    # Explicit unverified case
    if employer_name == "startup xyz":
        return {
            "verified": False,
            "employment_type": None,
            "years_in_business": 0
        }

    # Default case → SME
    return {
        "verified": True,
        "employment_type": "SME",
        "years_in_business": 5
    }
