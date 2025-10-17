통합감시실 설비 유지보수 저장소 (HSL Integrated Ops)

광명 통합감시실 및 광명/구로 관제실 설비의 유지보수 문서를 버전 관리합니다.
문서-우선(Documentation-First) 원칙으로 SOP/런북/체크리스트/도면/인벤토리를 표준화하고, 변경과 장애 이력을 투명하게 축적합니다.

목차

1. 시스템 개요

2. 네트워크 개요

2.1 전체 네트워크 구성도

2.2 통합감시실 네트워크 구성도

2.3 VLAN/서브넷 요약

2.4 핵심 라우팅/이중화(요약)

3. 서버·스토리지·SAN

4. 운영 절차(핵심)

5. 예방점검 & 장애 대응

6. 인벤토리 & 도면 원본

7. 문서 사이트(선택)

8. 변경관리/보안

9. 로드맵

1. 시스템 개요

범위: 고속선 종합감시제어시스템 중 광명 통합감시실 및 광명/구로 관제실 설비

핵심 설비:

서버: HP DL580 G3, HP DL360 G4p, (미디어/DB/EMS/NMS/WEB)

스토리지: HP EVA8000(FATA 500GB ×168, DiskGroup×2, VRAID5), SAN Switch 2/16V(이중 패브릭)

SW: Windows Server 2003(Std/Ent, MSCS), MS SQL 2000, Oracle 10g, Omniworker5, V3Net

운영 원칙: 문서-우선, 변경 이력화, 정기 점검+복구 리허설, 최소 권한/암호 금고관리

자세한 장비/소프트웨어 매트릭스는 docs/overview/system-summary.md
 참고.

2. 네트워크 개요

본 절은 첨부된 네트워크 구성도를 기반으로 주소체계/VLAN/이중화를 요약합니다.
정확한 IP는 inventory/ipam.csv 및 현장 라우터/스위치 설정과 일치시켜 관리합니다.

2.1 전체 네트워크 구성도

통합감시실과 15개 통신실을 기준으로 한 전체 구성

주요 특징

서버 존(VLAN10), 디스플레이/단말 존(VLAN20), 코어/링크 존(VLAN30 & P2P /29) 분리

코어 이중화(L3 스위치/백본/방화벽 이중 구성), 관제실(광명/구로)로 전용 구간 연결

통신실 #1~#16 구간은 백본 라우터를 통해 허브-앤-스포크 형태로 연동

2.2 통합감시실 네트워크 구성도

각 서버 역할별 VLAN 분리 + 백본스위치 이중화로 단일 장애 시 우회경로 확보

서버군(예): 메인/DB/미디어/EMS/NMS/WEB, SAN/스토리지 서버
외부 연동: 관제실(광명/구로), 통신실(#1~#16), 백본 라우터/방화벽을 통한 구간 분리

2.3 VLAN/서브넷 요약
VLAN	용도/세그먼트	주소계획(도면 기준)	비고
VLAN10	서버 존(메인/DB/미디어/EMS/NMS/WEB 등)	10.145.91.1 ~ 10.145.91.62 /26	게이트웨이 VRRP(VIP) 사용
VLAN20	Display / 단말 존	10.145.91.65 ~ 10.145.91.126 /26	대형 디스플레이/콘솔
VLAN30	코어/인프라(코어–L3–FW 링크용)	/29 P2P 블록(예: 10.145.91.129/29, 10.145.91.137/29, 10.145.91.145/29, 10.145.91.153/29 등)	코어/라우터/방화벽 사이 포인트투포인트

※ 상기 블록은 도면 표기 기준의 예시입니다. 실제 운용 값은 inventory/ipam.csv 및 장비 설정에 맞춰 검증/정합 유지가 필요합니다.

2.4 핵심 라우팅/이중화(요약)

코어 스위치(이중): VLAN10/20/30 인터페이스 보유, VRRP로 게이트웨이 가상 IP 제공

예시) VLAN10: VRRP VIP 10.145.91.1/26, 코어1/코어2는 각자 INT IP 보유

예시) VLAN20: VRRP VIP 10.145.91.65/26

코어–L3–FW–백본 라우터 간은 /29 P2P 링크로 상호 이중 경로 구성

관제실(광명/구로): 관제망 구간으로 분리, 필요한 서비스 포트만 방화벽 정책으로 허용

통신실(#1~#16): 백본 라우터 경유 허브-앤-스포크, 각 통신실 라우터/스위치와 정적/동적 라우팅 정책 연동

3. 서버·스토리지·SAN

EVA8000: FATA 500GB ×168 → DiskGroup×2(VRAID5, Spare=single), 여유율 상시 모니터링

SAN: StorageWorks 2/16V ×2 (이중 패브릭), Single-Initiator Zoning 권장

미디어서버 이중화: (MEDIA1,2)=Cluster1 / (MEDIA3,4)=Cluster2, MSCS(WS2003 Ent.)

구성 상세는 아래 문서를 참조하세요.

docs/storage/eva-overview.md

docs/storage/zoning-policy.md

docs/cluster/mscs-cluster.md

4. 운영 절차(핵심)

전원 시퀀스: SAN → EVA → 서버 (기동) / 서버 → EVA → SAN (종료)

EVA 관리 접속: 관리서버 → IE → http://127.0.0.1:2301 → 기본계정 즉시 변경 필수

LED 치트시트: DL580/DL360 Health LED(녹=정상, 황=주의, 적=위험), NIC 링크/트래픽 상태 확인

문서:

docs/operations/power-sequence.md

docs/hardware/led-cheatsheet.md

5. 예방점검 & 장애 대응

일일/주간/월간/분기 체크리스트: EVA/SAN/클러스터/백업/로그 상태 점검

런북(예): NIC 링크 불량, HBA 경로 장애, 디스크 장애, 클러스터 노드 다운

문서:

docs/operations/maintenance-checklists.md

docs/operations/incident-runbooks.md

6. 인벤토리 & 도면 원본

인벤토리: inventory/assets.yaml
, inventory/ipam.csv

점검 스크립트: python scripts/validate_inventory.py

도면 원본: diagrams/*.drawio, diagrams/*.mmd

렌더 결과(svg/png)도 함께 보관(버전별 변화 추적)

7. 문서 사이트(선택)

MkDocs + Material 테마로 내부 문서 사이트를 구동할 수 있습니다.

pip install mkdocs mkdocs-material
mkdocs serve   # 로컬 미리보기
mkdocs build   # /site 생성


구성: mkdocs.yml

8. 변경관리/보안

모든 변경은 PR로 수행, 영향도/롤백/테스트 필수

EVA/관리서버 등 기본 계정 즉시 변경, 금고 보관/로테이션 정책 준수

보안 정책 요약: SECURITY.md
 / 기여 규칙: CONTRIBUTING.md

변경 이력: CHANGELOG.md

9. 로드맵

인벤토리 정합성 확정(통신실 포함), Zoning 세부/WWPN 매핑 문서화

EVA 여유 용량 확보(아카이빙/증설/정리), DR 리허설 표준화(RPO/RTO)

관제실/통신실 간 트래픽 정책 및 포트 매트릭스 정리

세부 항목: ROADMAP.md

부록: 빠른 참조

게이트웨이(VRRP): VLAN10 10.145.91.1/26, VLAN20 10.145.91.65/26 (도면 기준 예시, 현장값으로 검증 필요)

코어/P2P: 10.145.91.129/29, .137/29, .145/29, .153/29 등 (코어–L3–FW 링크)

관제실 연결: 광명/구로 관제망으로 분리, 방화벽 정책 최소 허용
