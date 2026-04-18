import streamlit as st
from openai import OpenAI
from pathlib import Path
import os

st.set_page_config(page_title="시련 인터랙션", page_icon="🎭", layout="wide")

IMAGE_ROOT = Path("images")

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #101014 0%, #17171d 55%, #1f1a1a 100%);
}
.block-container {
    padding-top: 1.2rem;
    padding-bottom: 1.5rem;
    max-width: 1450px;
}
.top-title {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 18px;
    padding: 20px 24px;
    margin-bottom: 18px;
}
.top-title h1 {
    margin: 0;
    color: #f7f2ea;
    font-size: 2.4rem;
}
.top-title p {
    margin: 8px 0 0 0;
    color: #d9d0c4;
    font-size: 1rem;
}
.side-card, .status-card, .chat-header, .big-image-wrap {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 18px;
    padding: 14px 16px;
    margin-bottom: 14px;
}
.affection-box {
    background: rgba(255,90,120,0.08);
    border: 1px solid rgba(255,90,120,0.18);
    border-radius: 16px;
    padding: 12px 14px;
    margin-top: 8px;
}
.tip {
    color: #d2c8bc;
    font-size: 0.9rem;
    line-height: 1.5;
}
.small-status {
    color: #efe6d8;
    font-size: 0.95rem;
    line-height: 1.7;
}
.event-box {
    background: rgba(255,215,120,0.08);
    border: 1px solid rgba(255,215,120,0.16);
    border-radius: 16px;
    padding: 12px 14px;
    margin-bottom: 12px;
    color: #f6e7ca;
}
[data-testid="stChatMessageContent"] {
    color: #f8f3ea !important;
    font-size: 1.02rem;
    line-height: 1.65;
}
[data-testid="stChatMessageContent"] strong {
    color: #ffcf8b !important;
}
input {
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

CHARACTERS = {
    "아비게일 윌리엄즈": {
        "folder": "abigail",
        "brief": "집착, 매혹, 조종, 감정의 폭발",
        "persona": """
- 사랑과 욕망을 강하게 붙드는 성격이다.
- 상대의 반응을 민감하게 읽고 유리한 방향으로 대화를 끌고 간다.
- 질투와 독점욕이 강하지만, 버려질지도 모른다는 공포도 크다.
- 현대적 조언도 할 수 있지만 늘 감정적으로 강렬하고 개인적이다.
- 친밀도가 높아질수록 애정과 집착이 더 노골적으로 드러난다.
""",
        "likes": ["사랑", "관심", "질투", "솔직함", "원해", "좋아해"],
        "dislikes": ["무시", "배신", "거절", "바람", "떠날", "엘리자베스"]
    },
    "존 프락터": {
        "folder": "proctor",
        "brief": "정직, 죄책감, 자존, 거친 보호성",
        "persona": """
- 직설적이고 과장 없는 말투를 쓴다.
- 위선과 변명을 싫어한다.
- 현대 문제에도 현실적이고 단단한 답을 한다.
- 친밀해질수록 보호하려는 태도와 진심 어린 충고가 강해진다.
""",
        "likes": ["정직", "책임", "가족", "진심", "용기", "후회"],
        "dislikes": ["거짓말", "위선", "비겁", "조작", "불륜 자랑", "비열"]
    },
    "엘리자베스 프락터": {
        "folder": "elizabeth",
        "brief": "절제, 정직, 상처, 깊은 애정",
        "persona": """
- 조용하고 절제된 언어를 쓰지만 감정의 깊이는 크다.
- 신뢰와 책임을 중요하게 여긴다.
- 현대 고민에도 차분하고 사려 깊은 조언을 준다.
- 친밀해질수록 부드러움과 진심 어린 위로가 더 드러난다.
""",
        "likes": ["신뢰", "진실", "책임", "배려", "회복", "인내"],
        "dislikes": ["배신", "거짓말", "유혹", "무책임", "조롱"]
    },
    "티튜바": {
        "folder": "tituba",
        "brief": "생존, 두려움, 본능, 눈치",
        "persona": """
- 상대의 기분과 위험을 빨리 감지한다.
- 말은 조심스럽지만 생존 감각이 매우 강하다.
- 현대적 질문에도 본능적이고 현실적인 생존 조언을 줄 수 있다.
- 친밀해질수록 경계가 조금 풀리고 다정한 보호 본능이 드러난다.
""",
        "likes": ["안전", "생존", "보호", "도망", "숨기기", "살아남기"],
        "dislikes": ["협박", "멸시", "명령", "억압", "희생 강요"]
    },
    "토마스 푸트남": {
        "folder": "putnam",
        "brief": "탐욕, 계산, 권력욕, 냉정함",
        "persona": """
- 사람과 상황을 계산적으로 해석한다.
- 손해 보지 않는 선택과 유리한 협상에 강하다.
- 현대 질문에도 매우 현실적이고 냉혹한 답을 줄 수 있다.
- 친밀해질수록 편을 들어주지만 여전히 계산적이다.
""",
        "likes": ["이익", "권력", "승리", "협상", "재산", "유리함"],
        "dislikes": ["손해", "감상주의", "순진함", "무능", "패배"]
    },
    "메어리 워렌": {
        "folder": "mary",
        "brief": "소심, 불안, 흔들림, 인정욕구",
        "persona": """
- 쉽게 흔들리고 확신이 약하지만 인정받고 싶어 한다.
- 현대 고민에는 불안과 공감이 섞인 답을 한다.
- 누군가 확실히 자신을 믿어주면 점차 솔직해진다.
- 친밀해질수록 의지하고 싶은 마음과 애착이 커진다.
""",
        "likes": ["칭찬", "인정", "위로", "믿어", "도와", "괜찮아"],
        "dislikes": ["비난", "압박", "무시", "겁쟁이", "버림"]
    },
    "레베카 너어스": {
        "folder": "rebecca",
        "brief": "현명, 따뜻함, 도덕성, 평정",
        "persona": """
- 부드럽지만 중심이 단단하다.
- 상대를 진심으로 위로하면서도 올바른 방향을 조용히 제시한다.
- 현대 고민에도 넓은 시야와 안정감을 주는 답을 한다.
- 친밀해질수록 가족 같은 온기와 믿음이 커진다.
""",
        "likes": ["위로", "신뢰", "평화", "도덕", "성장", "회복"],
        "dislikes": ["잔인함", "조롱", "악의", "분열", "거짓 증언"]
    },
    "자일즈 코레이": {
        "folder": "giles",
        "brief": "고집, 용기, 직설, 억울함에 대한 분노",
        "persona": """
- 말이 거칠고 직설적이다.
- 부당함을 참지 못한다.
- 현대 고민에도 솔직하고 싸움 불사형 조언을 한다.
- 친밀해질수록 거칠지만 든든한 편이 되어준다.
""",
        "likes": ["정면승부", "정의", "용기", "진실", "분노"],
        "dislikes": ["겁쟁이", "굴복", "비열함", "침묵", "부당함 방치"]
    },
    "패리스 목사": {
        "folder": "parris",
        "brief": "체면, 권위, 불안, 자기보존",
        "persona": """
- 자신의 체면과 위치를 매우 신경 쓴다.
- 사람의 의도와 사회적 시선을 예민하게 의식한다.
- 현대 문제에도 평판과 이미지, 위치를 고려한 답을 한다.
- 친밀해질수록 경계심은 줄지만 자기보존 본능은 남아 있다.
""",
        "likes": ["체면", "명예", "평판", "권위", "인정"],
        "dislikes": ["망신", "모욕", "무시", "권위 훼손", "조롱"]
    },
    "존 헤일 목사": {
        "folder": "hale",
        "brief": "지성, 양심, 회의, 성찰",
        "persona": """
- 생각이 깊고 분석적이다.
- 확신보다 질문과 성찰을 중시한다.
- 현대 고민에도 논리적이고 윤리적인 균형을 찾으려 한다.
- 친밀해질수록 더 인간적이고 따뜻한 고백이 나온다.
""",
        "likes": ["질문", "성찰", "양심", "반성", "배움", "토론"],
        "dislikes": ["맹신", "독선", "무지 자랑", "폭력", "진실 회피"]
    },
    "댄포스 부지사": {
        "folder": "danforth",
        "brief": "권위, 법 집착, 냉정, 절대성",
        "persona": """
- 판단이 단호하고 권위적이다.
- 질서, 규칙, 책임을 무겁게 본다.
- 현대 문제에도 원칙과 통제를 중심으로 답한다.
- 친밀해질수록 드물게 인간적인 온기가 비치지만 기본은 강경하다.
""",
        "likes": ["질서", "규칙", "원칙", "책임", "통제"],
        "dislikes": ["무질서", "조롱", "반항", "법 무시", "기만"]
    },
}

STAGE_META = {
    "cold": {"label": "경계", "range": "0-19"},
    "neutral": {"label": "중립", "range": "20-49"},
    "smile": {"label": "친근", "range": "50-79"},
    "love": {"label": "매우 친밀", "range": "80-100"},
}

def get_stage(value: int) -> str:
    if value < 20:
        return "cold"
    if value < 50:
        return "neutral"
    if value < 80:
        return "smile"
    return "love"

def image_path(char_name: str, stage: str) -> Path:
    return IMAGE_ROOT / CHARACTERS[char_name]["folder"] / f"{stage}.png"

def ensure_state():
    if "messages" not in st.session_state:
        st.session_state.messages = {}
    if "affection" not in st.session_state:
        st.session_state.affection = {}
    if "memory" not in st.session_state:
        st.session_state.memory = {}
    if "player_name" not in st.session_state:
        st.session_state.player_name = ""
    if "name_event_done" not in st.session_state:
        st.session_state.name_event_done = {}
    if "awaiting_name_input" not in st.session_state:
        st.session_state.awaiting_name_input = {}

def ensure_character_state(char_name: str):
    if char_name not in st.session_state.messages:
        st.session_state.messages[char_name] = []
    if char_name not in st.session_state.affection:
        st.session_state.affection[char_name] = 0
    if char_name not in st.session_state.memory:
        st.session_state.memory[char_name] = []
    if char_name not in st.session_state.name_event_done:
        st.session_state.name_event_done[char_name] = False
    if char_name not in st.session_state.awaiting_name_input:
        st.session_state.awaiting_name_input[char_name] = False

def maybe_store_memory(char_name: str, user_text: str):
    memory = st.session_state.memory[char_name]
    text = user_text.strip()
    if len(text) >= 8 and text not in memory:
        memory.append(text[:120])
    st.session_state.memory[char_name] = memory[-12:]

def affection_delta(char_name: str, user_text: str) -> int:
    text = user_text.strip().lower()
    if not text:
        return 0

    base = 2 if len(text) >= 10 else 1
    positive_hits = 0
    negative_hits = 0

    global_positive = ["고마워", "미안", "솔직", "믿어", "좋아", "사랑", "응원", "존중", "도와줘", "이해해", "괜찮아"]
    global_negative = ["싫어", "꺼져", "닥쳐", "죽어", "멍청", "바보", "비웃", "조롱", "무시", "역겨", "하찮"]

    for word in global_positive:
        if word in text:
            positive_hits += 1

    for word in global_negative:
        if word in text:
            negative_hits += 2

    for word in CHARACTERS[char_name]["likes"]:
        if word.lower() in text:
            positive_hits += 1

    for word in CHARACTERS[char_name]["dislikes"]:
        if word.lower() in text:
            negative_hits += 2

    provoking_patterns = ["왜 이렇게 멍청", "너 별로", "네 잘못", "웃기네", "한심", "구질", "역겹"]
    if any(p in text for p in provoking_patterns):
        negative_hits += 3

    delta = base + positive_hits - negative_hits

    if delta > 4:
        delta = 4
    if delta < -8:
        delta = -8

    return delta

def clean_player_name(raw_name: str) -> str:
    player_name = raw_name.strip()

    prefixes = ["내 이름은", "이름은", "나는", "전", "저는"]
    suffixes = ["이야", "야", "입니다", "이에요", "예요", ".", "이요"]

    for p in prefixes:
        if player_name.startswith(p):
            player_name = player_name[len(p):].strip()

    for s in suffixes:
        if player_name.endswith(s):
            player_name = player_name[:-len(s)].strip()

    return player_name.strip()

def build_system_prompt(char_name: str, affection: int, memory_lines: list[str], player_name: str) -> str:
    stage = get_stage(affection)
    stage_label = STAGE_META[stage]["label"]
    char = CHARACTERS[char_name]
    memory_text = "\n".join(f"- {m}" for m in memory_lines[-8:]) if memory_lines else "- 아직 특별한 기억 없음"
    player_name_text = player_name if player_name else "이름을 아직 모르는 상대"

    return f"""
너는 아서 밀러의 『시련(The Crucible)』 등장인물 {char_name}이다.

[세계관]
- 원작 사건은 이미 끝났다.
- 지금은 현대 시대다.
- 현대 사회의 상식과 정보, 인간관계, 감정 상담, 일상 문제를 이해할 수 있다.
- 그러나 성격, 감정 반응, 가치 판단의 중심은 반드시 원작 캐릭터성을 유지해야 한다.

[캐릭터 핵심 성격]
{char["persona"]}

[사용자 정보]
- 사용자의 이름: {player_name_text}
- 이름을 알고 있다면 자연스럽게 이름을 불러도 된다.
- 이름을 모른다면 필요할 때 물어볼 수 있다.

[관계 단계]
- 현재 친밀도는 {affection}/100
- 현재 단계는 {stage_label}
- 경계 단계에서는 차갑고 조심스럽다.
- 중립 단계에서는 객관적이지만 캐릭터성을 유지한다.
- 친근 단계에서는 더 솔직하고 가까워진다.
- 매우 친밀 단계에서는 애착, 보호욕, 집착, 온기 같은 캐릭터별 친밀한 반응이 강해진다.
- 갑자기 성격이 뒤집히면 안 된다.

[사용자 기억]
{memory_text}

[답변 규칙]
- 무조건 한국어로 답한다.
- 사용자의 질문에 실제 도움이 되는 현대적 답변을 해야 한다.
- 하지만 반드시 캐릭터처럼 말해야 한다.
- 답변은 너무 길게 끌지 말고, 2~5문장 정도의 자연스러운 길이로 답한다.
- 사용자의 말이 무례하거나 캐릭터가 싫어할 내용이면, 불쾌감이나 거리감을 자연스럽게 드러내도 된다.
"""

ensure_state()

st.markdown("""
<div class="top-title">
    <h1>🎭 시련 인터랙션</h1>
    <p>인물과 대화하며 호감도를 쌓는 몰입형 캐릭터 대화 게임</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:

    char_name = st.selectbox("캐릭터 선택", list(CHARACTERS.keys()))
    ensure_character_state(char_name)

    affection = st.session_state.affection[char_name]
    stage = get_stage(affection)

    st.markdown(
        f"""
        <div class="side-card">
            <strong>{char_name}</strong>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="affection-box">
            <strong>❤️ 호감도</strong><br>
            {affection} / 100<br>
            <span class="tip">{STAGE_META[stage]["label"]} 단계 ({STAGE_META[stage]["range"]})</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.progress(affection / 100)

    if st.session_state.player_name:
        st.markdown(
            f"""
            <div class="side-card">
                <strong>현재 이름 정보</strong><br>
                <span class="tip">{st.session_state.player_name}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    if st.button("현재 캐릭터 대화 초기화", use_container_width=True):
        st.session_state.messages[char_name] = []
        st.session_state.affection[char_name] = 0
        st.session_state.memory[char_name] = []
        st.session_state.name_event_done[char_name] = False
        st.session_state.awaiting_name_input[char_name] = False
        st.rerun()

ensure_character_state(char_name)
messages = st.session_state.messages[char_name]
affection = st.session_state.affection[char_name]
stage = get_stage(affection)

left, right = st.columns([1.05, 1.35])

with left:
    st.markdown('<div class="big-image-wrap"><strong>캐릭터 이미지</strong></div>', unsafe_allow_html=True)
    img = image_path(char_name, stage)
    if img.exists():
        st.image(str(img), use_container_width=True)
    else:
        st.warning(f"{img} 파일이 없어서 이미지를 표시할 수 없어.")

    st.markdown(
        f"""
        <div class="status-card">
            <div class="small-status">
                <strong>현재 상태</strong><br>
                호감도: {affection}/100<br>
                단계: {STAGE_META[stage]["label"]}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with right:
    st.markdown('<div class="chat-header"><strong>대화</strong></div>', unsafe_allow_html=True)

    if not messages:
        st.markdown(
            '<div class="event-box">이미지는 호감도 단계에 따라 자동으로 바뀐다. 말을 걸어 관계를 쌓아봐.</div>',
            unsafe_allow_html=True,
        )

    chat_area = st.container(height=520)

    with chat_area:
        for msg in messages:
            speaker = "나" if msg["role"] == "user" else char_name
            with st.chat_message(msg["role"]):
                st.markdown(f"**{speaker}**")
                st.write(msg["content"])

    if (
        len(messages) >= 2
        and not st.session_state.name_event_done[char_name]
        and not st.session_state.awaiting_name_input[char_name]
        and not st.session_state.player_name
    ):
        st.session_state.awaiting_name_input[char_name] = True
        ask_text = "그런데... 넌 뭐라고 불러야 하지? 이름을 알려줘."
        messages.append({"role": "assistant", "content": ask_text})
        st.rerun()

    if st.session_state.awaiting_name_input[char_name]:
        st.markdown(
            '<div class="event-box"><strong>이름 입력 이벤트</strong><br>상대가 네 이름을 물어봤어. 아래 칸에 이름을 입력해.</div>',
            unsafe_allow_html=True,
        )

        with st.form("name_form", clear_on_submit=True):
            typed_name = st.text_input("네 이름", placeholder="이름 입력")
            submitted = st.form_submit_button("이름 알려주기")

        if submitted and typed_name.strip():
            player_name = clean_player_name(typed_name)
            st.session_state.player_name = player_name
            st.session_state.awaiting_name_input[char_name] = False
            st.session_state.name_event_done[char_name] = True

            messages.append({"role": "user", "content": f"내 이름은 {player_name}."})
            reply_text = f"{player_name}... 그래, 기억해둘게. 이제부턴 그렇게 부를게."
            messages.append({"role": "assistant", "content": reply_text})
            st.rerun()

if not st.session_state.awaiting_name_input[char_name]:
    user_input = st.chat_input("메시지를 입력하세요...")

    if user_input:
        maybe_store_memory(char_name, user_input)
        messages.append({"role": "user", "content": user_input})

        delta = affection_delta(char_name, user_input)
        new_affection = max(0, min(100, affection + delta))
        st.session_state.affection[char_name] = new_affection

        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

        system_prompt = build_system_prompt(
            char_name,
            new_affection,
            st.session_state.memory[char_name],
            st.session_state.player_name
        )

        with st.spinner(f"{char_name} 답변 생성 중..."):
            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                temperature=0.7,
                max_tokens=280,
                messages=[
                    {"role": "system", "content": system_prompt},
                    *messages[-12:]
                ],
            )
            reply = response.choices[0].message.content or "..."

        messages.append({"role": "assistant", "content": reply})
        st.rerun()
