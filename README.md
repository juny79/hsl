# HSL Integrated Ops — 통합감시실 설비 유지보수

고속선 **통합감시실** 및 **광명/구로 관제실** 설비의 운영 문서를 버전관리합니다.  
서버·스토리지·SAN·네트워크·SOP/런북·인벤토리를 한 곳에서 관리합니다.

문서 바로가기:  
[개요](docs/overview/system-summary.md) · [Topology](docs/overview/topology.md) · [EVA/SAN](docs/storage/eva-overview.md) · [Zoning](docs/storage/zoning-policy.md) · [체크리스트](docs/operations/maintenance-checklists.md) · [런북](docs/operations/incident-runbooks.md)

---

## 1. 네트워크 개요

### 1.1 전체 네트워크 구성도
(통합감시실 + 15개 통신실 기준)

![전체 네트워크 구성도](diagrams/전체네트워크구성도.png)

### 1.2 통합감시실 네트워크 구성도
(서버 역할별 VLAN 분리 + 백본 이중화)

![통합감시실 네트워크 구성도](diagrams/통합감시실-네트워크-구성도.png)

### 1.3 VLAN / 서브넷 요약 (도면 기준 예시)
실제 값은 `inventory/ipam.csv`와 장비 설정을 정본으로 유지합니다.

| VLAN   | 용도                                | 주소/마스크 (예시) | 게이트웨이 (예시) | 비고            |
|--------|-------------------------------------|--------------------|------------------|-----------------|
| VLAN10 | 서버 존 (MAIN/DB/MEDIA/EMS/NMS/WEB) | 10.145.91.0/26     | 10.145.91.1      | VRRP VIP        |
| VLAN20 | Display / 콘솔                      | 10.145.91.64/26    | 10.145.91.65     | VRRP VIP        |
| VLAN30 | 코어 / P2P 링크                     | 다수의 /29         | -                | 코어–L3–FW–BB   |

---

## 2. 서버 · 스토리지 · SAN 요약

| 영역   | 구성                                  | 핵심 포인트                                         |
|--------|---------------------------------------|------------------------------------------------------|
| 서버   | HP DL580 G3 / DL360 G4p               | Windows Server 2003(Std/Ent), MSCS(Ent)             |
| 스토리지 | HP EVA8000                           | FATA 500GB×168 → DiskGroup×2, VRAID5, Spare=single  |
| SAN    | StorageWorks 2/16V ×2                 | 듀얼 패브릭, Single-Initiator Zoning 권장           |
| 클러스터 | (MEDIA1,2)=Cluster1 / (MEDIA3,4)=Cluster2 | 분기 1회 페일오버 리허설                           |

자세히: [EVA](docs/storage/eva-overview.md) · [Zoning](docs/storage/zoning-policy.md) · [MSCS](docs/cluster/mscs-cluster.md)

---

## 3. 운영 핵심 절차

- 전원 시퀀스  
  - 기동: SAN → EVA → 서버  
  - 종료: 서버 → EVA → SAN
- EVA 관리 접속: 관리서버 → IE → `http://127.0.0.1:2301` (기본 계정 즉시 변경)
- LED 확인: DL580/DL360 Health(녹=정상, 황=주의, 적=위험), NIC(링크/트래픽)

문서: [전원 시퀀스](docs/operations/power-sequence.md) · [LED 치트시트](docs/hardware/led-cheatsheet.md)

---

## 4. 예방점검 · 장애 대응

- 체크리스트  
  - 일일: 클러스터 이벤트 / EVA·패스 알람 / SAN 포트 에러 / 주요 서비스 로그  
  - 주간: DG 사용률·캐시 히트율 리포트 / 백업 성공 + 샘플 복구  
  - 월·분기: 펌웨어 검토 / 구성 백업 / 페일오버 리허설
- 런북(예): NIC 링크 불량 · HBA 경로 장애 · EVA 디스크 장애 · 클러스터 노드 다운

문서: [체크리스트](docs/operations/maintenance-checklists.md) · [런북](docs/operations/incident-runbooks.md)

---

## 5. 인벤토리 & 도면

- 자산/주소: `inventory/assets.yaml`, `inventory/ipam.csv`
- 정합성 검사:

```bash
python scripts/validate_inventory.py

- 도면 원본: `diagrams/*.drawio`, `diagrams/*.mmd`  
  *(렌더본 `diagrams/*.png` 또는 `diagrams/*.svg`도 함께 보관)*

---

## 6. 문서 사이트(선택) & 협업 규칙

### 6.1 MkDocs(Material) 로컬 미리보기
```bash
pip install mkdocs mkdocs-material
mkdocs serve
```

### 6.2 빌드
```bash
mkdocs build
```

### 6.3 협업 규칙
- 브랜치/PR: `main` 보호 → `feature/*`에서 PR, **영향도/롤백/테스트** 필수
- 변경 이력/가이드: [CHANGELOG](CHANGELOG.md) · [CONTRIBUTING](CONTRIBUTING.md)

---

## 7. 보안 메모
- EVA/관리서버 **기본 계정 즉시 변경**, 분기 로테이션·접근 로그 유지
- **최소 권한 원칙**, **금고 보관(2인 승인)**, **이동식매체 통제**
- 정책 문서: [SECURITY.md](SECURITY.md)

---

## 8. 로드맵(요약)
- [ ] 인벤토리 정합성(통신실 포함) 확정
- [ ] Zoning 상세(WWPN 매핑)·도면 업데이트
- [ ] EVA 여유율 확보(아카이빙/증설/정리)
- [ ] DR 리허설(RPO/RTO) 표준화

> 이 README의 네트워크 주소는 **도면 기반 예시**입니다.  
> 실제 운영 값은 `inventory/ipam.csv`와 장비 설정을 **정본**으로 유지하세요.

