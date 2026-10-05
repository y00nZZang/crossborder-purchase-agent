# Malltail 일본 배송신청 필드 지도

관측: 2026-09-29 현재 UI 4단계 중 1/2단계만 직접 조사. 3/4단계·소분류·복수 수량 단가 의미는 실행 시 확인 필요. 공식 https://post.malltail.com/buy_guides/use_introduce 안내의 단계 수는 UI와 다를 수 있다. 이 지도는 완성된 고정 selector 자동화가 아니다.

| 필드 | 출처 / 관측 ID 후보 |
| --- | --- |
| 센터·운송 | 판매점의 실제 센터 주소 / name=center, radio_av(항공), radio_sh(해상) |
| 스토어 URL·오더 넘버 | 주문 내역 / ordersShopUrl, ordersShopOrderNum |
| 상품 링크·일문/영문명·브랜드 | 공개 상품/주문 / goods_info_etc1, goods_info_name1, goods_info_brand1 |
| 금액·수량 | 원주문 실제 JPY / goods_info_price1, goods_info_quantity1 |
| 품목 대/소분류 | 현재 선택지 / tmp_goods_category_title1, goods_category1 |
| 운송장 | 발송 안내 / goods_info_tracking_number1 |
| 상품코드·색상·사이즈 | 실제 코드/선택 옵션 / goods_code1, goods_info_color1, goods_info_size1 |
| 이미지 | 공개 상품 이미지, 선택항목. 검수 조건 설명 필요 |
| 수령인·통관정보 | 승인된 저장 프로필. 현재 UI의 필수값과 동의를 직접 확인 |

ID는 관측 힌트다. 현재 라벨과 보이는 상품 행으로 범위를 먼저 한정한다. 숨겨진 템플릿이 여럿 있어 전체 input의 first/nth는 잘못된 행을 고를 수 있다. HTML required가 없다는 이유로 선택항목으로 해석하지 않는다. 브랜드에 아티스트를 자동 대입하지 않는다. CD/DVD 대분류 H는 영상매체에만 해당하며 다른 상품에 재사용하지 않는다.

센터는 사후 수정 제한, 입고 후 주문/수령 정보 수정 제한이 공식 안내에 있으므로 최신 정책 확인 후 제출 전 대조한다. 접수 완료 화면은 상품명/수량/금액·신청번호와 함께 확인한다. ‘상품이 물류센터에 도착하면 배송비를 측정’ 안내는 운임 확정 이전이라는 뜻이다. 이전 신청을 취소하지 않은 채 새 주문을 등록하면 별도 신청이 남을 수 있다.
