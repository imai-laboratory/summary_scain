from numpy import dot
from numpy.linalg import norm

def dummy_completion(prompt, encoding):
    text = "AとBは、それぞれの地元や住んでいる場所について話しています。田舎生まれのAにとっては、都会の東京がとても魅力的な場所であると感じているようです。"
    prompt_tokens = len(encoding.encode(prompt))
    completion_tokens = len(encoding.encode(text))
    total_tokens = prompt_tokens + completion_tokens
    response = {
        "id": "chatcmpl-123",
        "object": "chat.completion",
        "created": 1677652288,
        "choices": [{
        "index": 0,
        "message": {
            "role": "assistant",
            "content": text,
        },
        "finish_reason": "stop"
        }],
        "usage": {
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": total_tokens
        }
    }
    return response

def cosine_similarity(vector1, vector2):
    return dot(vector1, vector2)/(norm(vector1)*norm(vector2))