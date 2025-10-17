🛰️ HSL Integrated Ops — 통합감시실 설비 유지보수

광명 통합감시실 및 광명/구로 관제실의 서버·스토리지·SAN·네트워크 운영 문서를
문서-우선(Documentation-First) 방식으로 버전관리합니다.

🔗 Quick Links

📘 시스템 개요 → docs/overview/system-summary.md

🖧 네트워크 Topology → 아래 이미지 & docs/overview/topology.md

💾 EVA/SAN → docs/storage/eva-overview.md
 / docs/storage/zoning-policy.md

🧰 SOP·런북 → docs/operations/maintenance-checklists.md
 / docs/operations/incident-runbooks.md

🧾 인벤토리 → inventory/assets.yaml
 / inventory/ipam.csv

🗺️ 네트워크 한눈에 보기

전체 네트워크 구성도 (통합감시실 + 15개 통신실 기준)

<img src="diagrams/전체네트워크구성도.png" alt="전체 네트워크 구성도" width="100%"/>

통합감시실 네트워크 구성도 (서버역할별 VLAN 분리 + 백본 이중화)

<img src="diagrams/통합감시실-네트워크-구성도.png" alt="통합감시실 네트워크 구성도" width="100%"/>
🧩 VLAN / 서브넷 요약

실제 주소는 inventory/ipam.csv와 장비 설정을 정본으로 유지합니다. 아래는 도면 기준 요약(예시).

VLAN	용도	주소/마스크 (예)	게이트웨이(예)	비고
VLAN10	서버 존 (MAIN/DB/MEDIA/EMS/NMS/WEB)	10.145.91.0/26	10.145.91.1 (VRRP VIP)	핵심 서버 세그먼트
VLAN20	Display/콘솔	10.145.91.64/26	10.145.91.65 (VRRP VIP)	대형월·운영단말
VLAN30	코어/P2P 링크	다수의 /29 블록	코어–L3–FW–BB 링크	이중 경로

🔐 라우팅/이중화: 코어(이중)에서 VLAN IF 보유 + VRRP 제공 → L3/FW/BB는 /29 P2P로 상호 연결, 장애 시 우회 경로 확보.

🖥️ 서버·스토리지·SAN 한눈정리
영역	구성	핵심 포인트
서버	HP DL580 G3 / DL360 G4p	Win2003(Std/Ent), MSCS(Ent)
스토리지	HP EVA8000	FATA 500GB×168 → DiskGroup×2, VRAID5, Spare=single
SAN	StorageWorks 2/16V ×2	듀얼 패브릭, Single-Initiator Zoning 권장
클러스터	MEDIA(1,2)=Cluster1 / (3,4)=Cluster2	분기 1회 페일오버 리허설

📎 자세히: docs/storage/eva-overview.md
, docs/storage/zoning-policy.md
, docs/cluster/mscs-cluster.md

⚙️ 운영 핵심 절차

반드시 순서를 지켜 주세요.

전원 시퀀스

기동: SAN → EVA → 서버

종료: 서버 → EVA → SAN

EVA 관리 접속 (Command View)

관리서버 → IE → http://127.0.0.1:2301 → 로그인

⚠️ 기본 계정 즉시 변경 & 금고 관리

LED 치트시트

DL580/DL360 Health: 🟢=정상 / 🟡=주의 / 🔴=위험

NIC: 🟢=링크 / 깜빡임=트래픽 / 꺼짐=미연결

📘 절차 상세: docs/operations/power-sequence.md
 · docs/hardware/led-cheatsheet.md

🧪 예방점검 · 🛠️ 장애 대응

체크리스트

✅ 일일: 클러스터 이벤트, EVA/패스 알람, SAN 포트 에러, 주요 서비스 로그

📅 주간: DG 사용률/캐시 히트율 리포트, 백업 성공/샘플 복구

📆 월간/분기: 펌웨어 검토, 구성 백업, 페일오버 리허설

런북(예)

NIC 링크 불량 / HBA 경로 장애 / EVA 디스크 장애 / 클러스터 노드 다운

📘 문서: docs/operations/maintenance-checklists.md
 · docs/operations/incident-runbooks.md

📦 인벤토리 & 도면 원본

자산 & IPAM

python scripts/validate_inventory.py  # IP 형식/중복/정합 체크


inventory/assets.yaml
 · inventory/ipam.csv

도면 원본

diagrams/*.drawio, diagrams/*.mmd (렌더 png/svg 함께 보관)

🧰 개발자/문서 워크플로
<details> <summary><b>문서 사이트 (MkDocs, 선택)</b></summary>
pip install mkdocs mkdocs-material
mkdocs serve   # 로컬 미리보기
mkdocs build   # /site 생성


구성파일: mkdocs.yml

</details> <details> <summary><b>브랜치/PR 규칙</b></summary>

main 보호, 모든 변경은 feature/* → PR

PR에는 영향도/롤백/테스트 필수

커밋 접두: docs:, ops:, fix:, feat:, sec:, chore:

변경 이력: CHANGELOG.md
 · 기여 규칙: CONTRIBUTING.md

</details>
🔒 보안 메모

EVA/관리서버 등 기본 계정 즉시 변경, 분기 로테이션

관리자 권한 최소화 & 사유 로그, 금고 보관(2인 승인)

문서: SECURITY.md

🗺️ 로드맵 스냅샷

 인벤토리 정합성(통신실 포함) 확정

 Zoning 상세(WWPN 매핑) & 도면 업데이트

 EVA 여유율 확보(아카이빙/증설/정리)

 DR 리허설(RPO/RTO) 표준화

상세: ROADMAP.md

📌 부록: 실무 팁

VRRP VIP: VLAN10 10.145.91.1/26, VLAN20 10.145.91.65/26 (도면 기준 예시)

P2P 블록: 코어–L3–FW–백본 /29 링크(예: 10.145.91.129/29, .137/29, .145/29, .153/29 …)

관제실 연동: 광명/구로 관제망 별도, 최소 포트 허용 원칙

⚠️ 본 README의 주소는 도면 기반 요약입니다. 실제 운영 값은 inventory/ipam.csv & 장비 설정을 정본으로 관리합니다.

🙌 유지보수 조직 & 연락체계

(조직도 확정 시 삽입 예정 — 비상연락망/지원창구/승인권자)
