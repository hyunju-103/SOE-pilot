# SOE Fiscal Risk Tool — 최종 통합본

최종 통합 기준: `the earlier Full Logistic / EFC Only model` 및 `SOE-main_waterfall_v2_final(2).zip`.

## 선택한 방식
- 화면은 기존의 Home, Report, KPI Dashboard, Distress Indicator, Expected Fiscal Cost, Shock Scenarios, Government Support, Early Warning, Assumptions를 유지합니다.
- **Monte Carlo = Rating-anchored PD(기본, AAA 하한 + D 아래 logistic tail) + 단일 Logistic(민감도 비교) + EFC only**. 각 경로/연도의 Z-EM에 대해 20개 등급 PD를 정확히 지나는 단조 곡선(logit-PCHIP)으로 PD를 계산하며, 4.9 이상에서는 0.02%로 하한 고정하고, Z-EM -1.5(D 임계값) 아래에서는 40%에서 출발해 기울기 b(`pd_logit_b`)의 logistic tail을 따라 PD가 계속 상승합니다(Z-EM -3에서 약 72%, -7에서 약 99%). 결정론적 탭은 기존 등급별 PD를 그대로 씁니다.
- 민감도용 단일 Logistic: `PD = 1 / (1 + exp(-(a+b Z)))`, a = -2.02276962, b = -0.89133626 (상한 없는 minimax 적합, 최대 오차 6.50%p). 기존 Rating PD에 맞추어 추정했으나 실제 부도 이력으로 검증한 것은 아닙니다. 상한을 둔 이전 적합(a = -2.18031828, b = -1.10613960)은 `python scripts/calibrate_pd.py --refit --caps`로 재현할 수 있습니다.
- EFC = PD × EAD × LGD. 실제 부도 사건 및 실현 손실은 추첨하지 않습니다. 채무상환 미이행만으로 MC PD를 100%로 덮어쓰지 않습니다.
- 일반 Single Scenario의 PD 방식은 기존처럼 Rating 중심으로 유지합니다. UI에 선택창이 노출되지만 Monte Carlo 화면에서는 숨겨 혼동을 줄입니다.
- 기존 Rating PD·Rating-anchored(기본)·단일 Logistic(민감도) 비교표 및 곡선은 **Shock Scenarios > Distribution (Monte Carlo) > Rating PD comparison and calibration details**에서 열어 볼 수 있습니다.
- 현금흐름에서 채무상환이 지연되어도 단일 시나리오에서 곧바로 '부도'로 처리하지 않는 것이 기본값입니다. 단일 시나리오 민감도 분석용 'Treat missed debt service as default' 옵션은 유지했습니다.

## 실행 방법
1. **바로 사용:** ZIP 내부의 `SOE-Fiscal-Risk-Final.html`을 더블 클릭하여 Chrome/Edge 등에서 엽니다. 입력 데이터 없이도 샘플 포트폴리오가 나타납니다.
2. **직접 데이터 사용:** 화면 상단의 **Upload data**로 기존 업로드 양식의 CSV/Excel을 선택합니다. ZIP 내 데이터는 실제 SENELEC 공식 재무자료가 아니라 예시용입니다.
3. **Streamlit:** 의존성 설치 후 프로젝트 폴더에서 `streamlit run Home.py`를 실행합니다.
4. **HTML 재생성:** 프로젝트 폴더에서 `python report.py --demo --out my_tool.html`을 실행합니다.

## 검증
- Python 및 JavaScript 문법 검사: 통과.
- Waterfall v2 회귀 검사: 14,228개 통과 (기본값 변경으로 이전의 '자동 부도' 테스트는 옵션을 명시하도록 수정함).
- Fuel path / cash-first 검사: 19,346개 통과.
- Python 및 JavaScript 핵심 MC 계산: 기본(Rating-anchored)과 Logistic 민감도 각각에서 PD 및 EFC 관계 확인, 실현 부도 칼럼 없음.
- Chromium 브라우저 smoke test: 화면 탐색, Monte Carlo 실행, PD 그래프, CSV 버튼, JS 오류 확인 통과.
- 전체 대규모 JS/Python parity 테스트는 실행 시간 제한으로 완료하지 못했으며, 모든 시나리오/브라우저에 대한 완전한 검증으로 해석해서는 안 됩니다.

## 참고
샘플 데이터가 표시하는 금액과 PD는 시연용이며 SENELEC 실측치가 아닙니다. 등급 PD 20개 자체가 예시용 표이며(CCC+와 CCC는 PD가 같아 그 사이 구간은 평평함), 단일 Logistic 민감도는 CCC+ 등 일부 등급에서 최대 6.50%p 오차가 있으므로 보정의 타당성을 추가로 검토하기 전에는 실증적으로 검증된 PD로 인용하지 않는 것이 좋습니다.
