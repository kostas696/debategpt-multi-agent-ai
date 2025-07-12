debategpt/
├── agents/
│   ├── proponent.py
│   ├── opponent.py
│   └── moderator.py
├── tools/
│   ├── fallacy_detector.py
│   ├── tavily_search.py
│   └── persona_prompt_tool.py
├── state/
│   └── debate_state.py
├── graph/
│   └── debate_graph.py
├── app.py
├── .env
├── requirements.txt
├── README.md
└── assets/
    └── debate_diagram.png



pytest test/test_run.py -s

streamlit run streamlit_app.py
