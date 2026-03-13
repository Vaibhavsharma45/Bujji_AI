(venv) PS D:\Projects\Bujji_Ai> python main.py
╭───────────────────────────────────────────────────────────────╮
│                                                               │
│                 ██████╗ ██╗   ██╗     ██╗██╗                  │
│                 ██╔══██╗██║   ██║     ██║██║                  │
│                 ██████╔╝██║   ██║     ██║██║                  │
│                 ██╔══██╗██║   ██║██   ██║██║                  │
│                 ██████╔╝╚██████╔╝╚█████╔╝██║                  │
│                 ╚═════╝  ╚═════╝  ╚════╝ ╚═╝                  │
│           Personal AI Assistant  v3.0 — 13 Mar 2026           │
│                                                               │
╰───────────────────────────────────────────────────────────────╯
  [!] PICOVOICE_KEY missing — wake word disabled (use voice/text mode)

  Select mode:
    [w]  Wake word  — say 'Jarvis' to activate (requires Picovoice key)
    [v]  Voice      — always listening, speak directly
    [t]  Text       — type commands

  Mode: v
─────────────────────────────────────────────────────────────────                                                                                                          
  ✓ Voice mode — speak anytime
─────────────────────────────────────────────────────────────────                                                                                                          
  → Listening…

  You: hey google see whatsapp
  → Thinking…
[14:19:38] ERROR     brain             Agent error: Error code: 400 - {'error': {'message': 'tool call validation failed: attempted to call tool \'open_application{"app_name": "whatsapp"}\' which was not in request.tools', 'type': 'invalid_request_error', 'code': 'tool_use_failed', 'failed_generation': '<function=open_application{"app_name": "whatsapp"}></function>'}}
  BUJJI: Thoda alag tarike se boliye — jaise 'open gmail' ya 'calculate 25% of 4000'.

  → Listening…
  → Listening…

  You: hey google open youtube
  → Thinking…
  BUJJI: YouTube is now open.

  → Listening…
  → Listening…
  → Listening…
  → Listening…
Traceback (most recent call last):
  File "D:\Projects\Bujji_Ai\main.py", line 222, in <module>
    main()
  File "D:\Projects\Bujji_Ai\main.py", line 217, in main
    run_voice_mode()
  File "D:\Projects\Bujji_Ai\main.py", line 162, in run_voice_mode
    raw, sr_rate = listen_raw()
                   ^^^^^^^^^^^^
  File "D:\Projects\Bujji_Ai\voice.py", line 108, in listen_raw
    audio = _recognizer.listen(src, timeout=STT_TIMEOUT, phrase_time_limit=STT_PHRASE_LIMIT)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Projects\Bujji_Ai\venv\Lib\site-packages\speech_recognition\__init__.py", line 462, in listen
    for a in result:
  File "D:\Projects\Bujji_Ai\venv\Lib\site-packages\speech_recognition\__init__.py", line 494, in _listen
    buffer = source.stream.read(source.CHUNK)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Projects\Bujji_Ai\venv\Lib\site-packages\speech_recognition\__init__.py", line 193, in read
    return self.pyaudio_stream.read(size, exception_on_overflow=False)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Projects\Bujji_Ai\venv\Lib\site-packages\pyaudio\__init__.py", line 570, in read
    return pa.read_stream(self._stream, num_frames,
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
KeyboardInterrupt
(venv) PS D:\Projects\Bujji_Ai> 