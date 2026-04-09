#!/usr/bin/env python3
"""Deep Research via Google Gemini Interactions API with Google Search grounding.

Usage:
    python3 deep_research.py "your research question" [--output file.md] [--model gemini-2.5-flash]

Requires: GOOGLE_API_KEY environment variable or pass via --api-key
"""
import argparse
import os
import sys
import time

def main():
    parser = argparse.ArgumentParser(description="Deep Research via Gemini")
    parser.add_argument("query", help="Research question")
    parser.add_argument("--output", "-o", help="Output file path")
    parser.add_argument("--model", default="gemini-2.5-flash", help="Gemini model")
    parser.add_argument("--api-key", default=None, help="Google API key")
    args = parser.parse_args()

    api_key = args.api_key or os.environ.get("GOOGLE_API_KEY", "")
    if not api_key:
        print("Error: Set GOOGLE_API_KEY or pass --api-key", file=sys.stderr)
        sys.exit(1)

    from google import genai

    client = genai.Client(api_key=api_key)

    prompt = f"""You are a deep research analyst. Conduct thorough research on the following topic and produce a comprehensive report.

Topic: {args.query}

Requirements:
- Be thorough and detailed (aim for 2000+ words)
- Cite specific sources, products, papers, or companies
- Include comparisons and trade-offs where relevant
- Structure with clear headers and sections
- Include an executive summary at the top
- End with actionable recommendations
- Use markdown formatting

Produce the report now."""

    start = time.time()
    response = client.models.generate_content(
        model=args.model,
        contents=prompt,
        config={"tools": [{"google_search": {}}]},
    )
    elapsed = time.time() - start

    report = response.text
    footer = f"\n\n---\n_Generated via Gemini {args.model} + Google Search grounding in {elapsed:.1f}s_\n"
    report += footer

    if args.output:
        os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
        with open(args.output, "w") as f:
            f.write(report)
        print(f"Report saved to {args.output} ({len(report)} chars, {elapsed:.1f}s)")
    else:
        print(report)


if __name__ == "__main__":
    main()
