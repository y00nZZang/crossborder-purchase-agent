# 직구 과정 조사와 두 가지 도구 구현 — 윤장한

개인이 에이전트의 도움을 받아 상품 조사·주문·배송신청·통관을 어디까지 진행할 수 있는지, 구매 후 발생하는 국제운송비와 관세를 어떻게 추정할 수 있는지 살펴봤습니다. 실제 구매 시험은 배송대행 접수까지의 결과입니다.

## 구현한 도구

- **Codex 플러그인:** 이커머스와 배송대행 사이트의 조사·입력·결과 확인을 보조합니다. 최초 요청1회와 후속 입력6회로 배송대행 접수까지 진행했습니다. 구매 확인 후 일일 메일 추적을 등록하는 절차는10/6에0.1.1로 추가했습니다.
- **URL 분석기:** 상품 URL에서 상품·배송·관세 정보를 분석합니다. 입력창과 실제 결과 화면, TCG 운영 사례 및 주류 사양·산술 시험을 장표에 담았습니다.

## 이번 경험에 대한 생각

에이전트가 배송대행 입력을 간소화하는 이점은 확인했습니다. 소형·경량 상품1개의 당시 부분 견적에서는SAZO 경로의 확인 비용 합계가 더 낮아 구매대행이 유리하다고 느꼈습니다. 조건 차이가 남아 전체 소량 직구의 결론으로 확대하지 않았습니다.

도구의 포장·세금 추정 정확도와 비API 사이트 수집, 사업의 합배송 비용 최적화는 서로 다른 미확인 문제입니다. 추가 검증 계획으로 제시하지 않고 이번 구현의 범위로 구분했습니다. 마지막은 에이전트 커머스와 물류 노하우에 대한 개인적 생각으로 정리했습니다.

## 부록 · Jev 판단 모델 비교 실험

가정용·취미 범위에서 선별한 새93개에 대해 기존 단일 경로 Jev와 GPT-6 Luna를 비교했습니다. HS 후보 판단의 중앙 처리시간은0.645초/4.510초로 약7배 빨랐고, 추정 API 비용은57.1% 낮았습니다. 운영 서비스 도입이나 전체 URL 분석시간의 개선 결과는 아닙니다.

HSCodeComp는 실제 전자상거래 상품632개에 전문가가 HS 코드를 붙인 공개 평가 데이터셋입니다. [원본 데이터셋](https://huggingface.co/datasets/ATH-MaaS/HSCodeComp). 서비스 범위는 연구 초안이며 검증된 사조 정책으로 간주하지 않습니다.

판단 품질·답변률에는 차이가 남아 최종 관세 분류에는 추가 검토가 필요합니다. 슬라이드는 시간·비용과 판단 한계를 설명하고, 정확도·답변률·토큰·실패 사례는 공개 레포에서 확인할 수 있습니다. 이전전체94개, 서비스범위78개, 새93개를 별도로 보존합니다. 복수 경로·혼합 방식은 후속 비교에서 제외했습니다.

[최신 실험 설명·품질 지표](https://github.com/y00nZZang/product-catalog/blob/main/docs/service-scope-jev-experiment-2026-10-07.md) · [결과 노트북](https://github.com/y00nZZang/product-catalog/blob/main/notebooks/service-scope-results-2026-10-07.ipynb) · [실패 사례](https://github.com/y00nZZang/product-catalog/blob/main/notebooks/service-scope-failures-2026-10-07.json)

## 제출 자료

- [PDF — 18장 · Jev 부록3장](crossborder-portfolio.pdf)
- [편집용 PPTX](crossborder-portfolio.pptx)
- [원고와 출처](narrative.md)
- [사용자 입력 집계](interaction-count.md)
- [경험과 생각](closing-perspective.md)
- [플러그인 코드](https://github.com/y00nZZang/crossborder-purchase-agent)
- [분석기 코드](https://github.com/y00nZZang/product-catalog) · [데모](https://catalog.janghan.dev/)

문서개정2026-10-07. 구현 보조: Codex. 실구매1건과 입력7회는2026-10-05 기록이며 화면 조작 횟수·시간 절감률과 구분합니다.
