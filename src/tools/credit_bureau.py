"""
Credit Bureau Tool

Mock implementation of credit bureau integration for development.
"""

from langchain_core.tools import tool


@tool
def mock_credit_bureau(pan: str) -> dict | None:
    """
    This tool will be used to mock the credit bureau report check
    :param pan: pan number to check the credit bureau
    :return: credit score as int or None
    """
    pan_scores = {
      "QWERT1234Z": 812,
      "ZXCVB5678K": 645,
      "PLMKO9876N": 721,
      "ASDFG4321H": 589,
      "YUIOP2468L": 777,
      "HJKLQ1357R": 693,
      "NMBCD8642T": 834,
      "LKJHG9753P": 602,
      "TREWA1122S": 748,
      "VCXZB5566M": 681,
      "ABCDE1111F": 352,
      "FGHIJ2222K": 298,
      "KLMNO3333P": 375,
      "PQRST4444R": 410,
      "UVWXY5555T": 389,
      "ZABCD6666V": 265,
      "EFGHI7777X": 342,
      "JKLMN8888Z": 315
    }

    score = pan_scores.get(pan, 0)

    if score is None:
        return None

    # Risk categorization logic
    if score >= 700:
        risk = "low risk"
    elif score >= 500:
        risk = "medium risk"
    else:
        risk = "high risk"

    return {
        "credit_score": score,
        "risk_category": risk
    }
