# numismAIc

AI-powered system for analyzing numismatic auction listings.

# Coin Auction Evaluator

Experimental multi-agent system for analyzing coin auction lots and generating heuristic price estimates.

The system parses auction listings, identifies coins from text and images, retrieves historical comparable sales, and produces an estimated valuation range.

⚠️ **This project is experimental and intended for research and educational purposes only.**


# Overview

Coin auctions contain valuable market signals, but the information is distributed across many auction platforms and is often unstructured.

This project explores whether an AI multi-agent architecture can:

1. Parse auction lot pages
2. Identify the coin being sold
3. Search historical comparable sales
4. Estimate an average market value based on previous sales
5. Estimate a maximum rational bid

The goal is **decision support**, not automated trading or financial advice.


# Usage Example 

Run the evaluation by providing an auction lot URL.

Example:

Basic usage in strict year matching mode
```
python main.py \
  --url https://violity.com/ua/119606198-velikobritaniya-krona-1935-serebro-auns-28-28-gramm
```

Range mode search that allows not strick year matching and providing an allowed search range
```
python main.py \
  --url https://violity.com/... \
  --range-year-search \
  --year-delta 2
```

# Output

Output is a report file

---

# System Architecture

The system is built as a **multi-agent pipeline**.


Agent 1: Lot URL validator

↓

Agent 2: Lot Parser

↓

Agent 3: Coin Identification

↓

Agent 4: Historical Comps Search

↓

Agent 5: Comparable Sales Analysis

↓

Agent 6: Valuation Engine

↓

Agent 7: Report Preparation


## Disclaimer

This project is an experimental research tool designed to explore
automated analysis of coin auction listings.

The system generates heuristic price estimates and recommendations
based on publicly available information and machine learning models.

No warranty is provided regarding accuracy, completeness, or suitability
for financial decisions.

This software does not constitute financial, investment, or trading advice.

Users are solely responsible for any decisions made using this software.