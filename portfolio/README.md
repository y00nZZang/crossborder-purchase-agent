# 직구 과정 조사와 두 가지 도구 구현 — 윤장한

개인이 에이전트의 도움을 받아 상품 조사·주문·배송신청·통관을 어디까지 진행할 수 있는지, 구매 후 발생하는 국제운송비와 관세를 어떻게 추정할 수 있는지 살펴봤습니다. 실제 구매 시험은 배송대행 접수까지의 결과입니다.

## 구현한 도구

- **Codex 플러그인:** 이커머스와 배송대행 사이트의 조사·입력·결과 확인을 보조합니다. 최초 요청1회와 후속 입력6회로 배송대행 접수까지 진행했습니다. 구매 확인 후 일일 메일 추적을 등록하는 절차는10/6에0.1.1로 추가했습니다.
- **URL 분석기:** 상품 URL에서 상품·배송·관세 정보를 분석합니다. 입력창과 실제 결과 화면, TCG 운영 사례 및 주류 사양·산술 시험을 장표에 담았습니다.

## 이번 경험에 대한 생각

에이전트가 배송대행 입력을 간소화하는 이점은 확인했습니다. 소형·경량 상품1개의 당시 부분 견적에서는SAZO 경로의 확인 비용 합계가 더 낮아 구매대행이 유리하다고 느꼈습니다. 조건 차이가 남아 전체 소량 직구의 결론으로 확대하지 않았습니다.

도구의 포장·세금 추정 정확도와 비API 사이트 수집, 사업의 합배송 비용 최적화는 서로 다른 미확인 문제입니다. 추가 검증 계획으로 제시하지 않고 이번 구현의 범위로 구분했습니다. 마지막은 에이전트 커머스와 물류 노하우에 대한 개인적 생각으로 정리했습니다.

## 부록 · Jev 판단 모델 비교 실험

HS 후보 선택의 중앙 처리시간은 HF94개 표본에서6.4배, 실제 메루카리30개에서5.7배 빨랐습니다. 메루카리의 독립 GPT-6 Sol HS6 일치율은84%였고, HF 정답 정확도는Jev29.8%·Luna38.3%로 차이가 있었습니다. 모든 조건에서 같은 성능을 유지했다고 일반화하지 않고 품질·보류·시간·비용을 분리했습니다.

[공개 실험 설명](https://github.com/y00nZZang/product-catalog/blob/main/docs/jev-experiment-2026-10-06.md) · [코드·노트북](https://github.com/y00nZZang/product-catalog/tree/main/notebooks) · [정제 측정값](https://github.com/y00nZZang/product-catalog/blob/main/notebooks/two-datasets-results-2026-10-06.json)

실험 결과는2026-10-06이며 운영 서비스 도입이나 전체 URL 분석시간 개선 결과가 아닙니다.

## 제출 자료

- [PDF — 18장 · Jev 부록3장](crossborder-portfolio.pdf)
- [편집용 PPTX](crossborder-portfolio.pptx)
- [원고와 출처](narrative.md)
- [사용자 입력 집계](interaction-count.md)
- [경험과 생각](closing-perspective.md)
- [플러그인 코드](https://github.com/y00nZZang/crossborder-purchase-agent)
- [분석기 코드](https://github.com/y00nZZang/product-catalog) · [데모](https://catalog.janghan.dev/)

문서개정2026-10-06. 구현 보조: Codex. 실구매1건과 입력7회는2026-10-05 기록이며 화면 조작 횟수·시간 절감률과 구분합니다.
