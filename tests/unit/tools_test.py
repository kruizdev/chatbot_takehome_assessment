from app.tools.airline_pets import get_policy

def test_pet_policy_basic():
    out = get_policy("Delta", "dog", question="crate requirements?")
    assert "crate" in out["answer"].lower()
    assert out["citations"], "should include citations"
