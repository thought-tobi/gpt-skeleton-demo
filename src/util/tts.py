from elevenlabs import generate, play, Voice, set_api_key


def tts(voice: str, text: str):
    set_api_key("21fdb17dfad673dba6e622acd4fc46ae")
    voices = {
        "donald trump": "6gYZDEbOjI0JvdjKspHv",
        "snoop dogg": "RpSFkaZbsz2v2aO78CPw",
        "bella": "EXAVITQu4vr4xnSDxMaL"
    }
    audio = generate(
        text=text,
        voice=Voice(
            voice_id=voices[voice.lower()]
        )
    )
    play(audio)
