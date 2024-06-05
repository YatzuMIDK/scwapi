from fastapi import APIRouter

router = APIRouter()

def cheemsify(text: str) -> str:
    cheems_text = []
    for word in text.split():
        if len(word) > 1:
            cheems_word = ""
            for char in word:
                if char.lower() in "aeiou":
                    cheems_word += char + "m"
                else:
                    cheems_word += char
            cheems_text.append(cheems_word)
        else:
            cheems_text.append(word)
    return " ".join(cheems_text)

@router.get("/cheemsify/{text}")
def cheemsify_endpoint(text: str):
    return {"original": text, "cheemsified": cheemsify(text)}
