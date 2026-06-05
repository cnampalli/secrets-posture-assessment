"""Shared domain vocabulary for the matrix model — single source of truth.

Importable by every leaf model module (compliance, optimizer, resilience,
vendor_intel) and by report_logic without an import cycle: report_logic imports
the leaves, so the leaves must not import report_logic. These constants used to
be copy-pasted across those modules; drift between copies produced contradictory
numbers in the same report, so they live here once.
"""

# Posture-state severity for worst-state aggregation (a control's state is the
# worst among its mapped use cases). LOWER rank = worse / more blocking.
#
# UNKNOWN (a mapped use case with no assessment) ranks BELOW MET on purpose:
# data-absence must never be counted as MET, but a real deficiency
# (GAP/PARTIAL/PENDING) still surfaces ahead of "not yet assessed".
STATE_RANK = {"GAP": 0, "PARTIAL": 1, "PENDING": 2, "UNKNOWN": 3, "MET": 4}

# Vendor coverage strength. LOWER rank = stronger coverage.
COVERAGE_ORDER = {"NATIVE": 0, "ADD-ON": 1, "PARTNER": 2, "GAP": 3, "N/A": 4}

# Use-case target families in the matrix (functional / non-functional).
UC_TYPES = ("UC-F", "UC-N")
