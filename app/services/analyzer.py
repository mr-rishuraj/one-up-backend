import hashlib

def analyze_profile(profile_text: str) -> dict:
    """
    Deterministic pseudo-AI analysis.
    Same input → same output
    Different input → different output
    """

    # Create stable variation per input
    seed = int(hashlib.sha256(profile_text.encode()).hexdigest(), 16)
    score = 75 + (seed % 35)  # 55–89

    strengths_pool = [
        "Clear professional direction",
        "Relevant industry keywords present",
        "Readable and structured profile",
        "Consistent academic and career timeline",
        "Shows initiative through projects"
    ]

    weaknesses_pool = [
        "Lacks quantified achievements",
        "Headline could be more specific",
        "Experience descriptions are generic",
        "About section lacks storytelling",
        "Limited visible impact metrics"
    ]

    improvements_pool = [
        "Rewrite headline with a clear value proposition",
        "Add numbers and metrics to experience",
        "Strengthen About section with a short narrative",
        "Highlight key projects and outcomes",
        "Optimize keywords for target roles",
        "Emphasize leadership or ownership examples"
    ]

    def pick(pool, n):
        return [pool[(seed + i) % len(pool)] for i in range(n)]

    return {
        "score": score,
        "strengths": pick(strengths_pool, 3),
        "weaknesses": pick(weaknesses_pool, 3),
        "improvements": pick(improvements_pool, 5),
    }
