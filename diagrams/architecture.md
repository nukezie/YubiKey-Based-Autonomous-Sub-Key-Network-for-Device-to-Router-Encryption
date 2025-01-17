# System Architecture Diagrams

## High-Level Architecture

```mermaid
graph TB
    subgraph Client Layer
        D[Device]
        R[Router]
        A[Admin Interface]
    end

    subgraph Network Layer
        LB[Load Balancer]
        FW[Firewall]
    end

    subgraph Application Layer
        API[API Server]
        Auth[Auth Service]
        KM[Key Manager]
        Mon[Monitor Service]
    end

    subgraph Storage Layer
        DB[(PostgreSQL)]
        Cache[(Redis)]
        Vault[(Key Vault)]
    end

    subgraph Security Layer
        YK[YubiKey HSM]
        SSL[SSL/TLS]
        IDS[Intrusion Detection]
    end

    D --> FW
    R --> FW
    A --> FW
    FW --> LB
    LB --> API
    API --> Auth
    API --> KM
    Auth --> YK
    KM --> YK
    API --> DB
    API --> Cache
    KM --> Vault
    Mon --> API
    Mon --> DB
    SSL --> API
    IDS --> FW
```

## Key Management Flow

```mermaid
sequenceDiagram
    participant D as Device
    participant API as API Server
    participant Auth as Auth Service
    participant YK as YubiKey
    participant KM as Key Manager
    participant DB as Database

    D->>API: Request Authentication
    API->>Auth: Validate Request
    Auth->>YK: Verify YubiKey
    YK-->>Auth: Verification Result
    Auth-->>API: Auth Status
    API->>KM: Request Key Generation
    KM->>YK: Generate Sub-key
    YK-->>KM: Sub-key Generated
    KM->>DB: Store Key Metadata
    KM-->>API: Key Generation Complete
    API-->>D: Authentication Complete
```

## Monitoring Architecture

```mermaid
graph LR
    subgraph Services
        YN[YubiKey Network]
        YM[YubiKey Monitor]
    end

    subgraph Metrics
        P[Prometheus]
        G[Grafana]
    end

    subgraph Alerts
        AM[Alert Manager]
        Email[Email]
        Slack[Slack]
    end

    YN --> P
    YM --> P
    P --> G
    P --> AM
    AM --> Email
    AM --> Slack
```

## Backup and Recovery Flow

```mermaid
graph TD
    subgraph Backup Process
        B1[Initiate Backup]
        B2[Export Keys]
        B3[Backup Config]
        B4[Backup Database]
        B5[Create Archive]
        B6[Encrypt Backup]
    end

    subgraph Recovery Process
        R1[Decrypt Backup]
        R2[Extract Archive]
        R3[Restore Keys]
        R4[Restore Config]
        R5[Restore Database]
    end

    B1 --> B2
    B2 --> B3
    B3 --> B4
    B4 --> B5
    B5 --> B6

    R1 --> R2
    R2 --> R3
    R3 --> R4
    R4 --> R5
```

## Deployment Architecture

```mermaid
graph TB
    subgraph Infrastructure
        OS[Ubuntu Server]
        Docker[Docker Optional]
    end

    subgraph CoreServices
        Nginx[Nginx Server]
        Redis[Redis Cache]
        Postgres[PostgreSQL]
    end

    subgraph Application
        YNS[YubiKey Network Service]
        YMS[YubiKey Monitor Service]
        Sup[Supervisor]
    end

    subgraph Security
        SSL[SSL/TLS]
        FW[Firewall Rules]
        SEL[SELinux/AppArmor]
    end

    OS --> Docker
    Docker --> Nginx
    Docker --> Redis
    Docker --> Postgres
    OS --> Nginx
    OS --> Redis
    OS --> Postgres
    Nginx --> YNS
    Redis --> YNS
    Postgres --> YNS
    Nginx --> YMS
    Redis --> YMS
    Postgres --> YMS
    SSL --> Nginx
    FW --> Nginx
    SEL --> YNS
    SEL --> YMS
    Sup --> YNS
    Sup --> YMS
```

## Authentication Flow

```mermaid
sequenceDiagram
    participant D as Device
    participant R as Router
    participant API as API Server
    participant YK as YubiKey
    participant DB as Database

    D->>R: Request Connection
    R->>API: Forward Request
    API->>YK: Verify Device Key
    YK-->>API: Verification Result
    API->>DB: Log Authentication
    API-->>R: Auth Response
    R-->>D: Connection Status
```

## Network Topology

```mermaid
graph TB
    subgraph External Network
        D1[Device 1]
        D2[Device 2]
        D3[Device 3]
    end

    subgraph DMZ
        R1[Router 1]
        R2[Router 2]
        LB[Load Balancer]
    end

    subgraph Internal Network
        API[API Servers]
        DB[(Databases)]
        YK[YubiKey HSM]
    end

    D1 --> R1
    D2 --> R1
    D3 --> R2
    R1 --> LB
    R2 --> LB
    LB --> API
    API --> DB
    API --> YK
```

## Key Rotation Process

```mermaid
stateDiagram-v2
    [*] --> Active
    Active --> Rotating: Rotation Time
    Rotating --> GeneratingNew: Generate New Key
    GeneratingNew --> Transitioning: Key Generated
    Transitioning --> Verifying: Update Systems
    Verifying --> Active: Verification Complete
    Verifying --> Failed: Verification Failed
    Failed --> Rotating: Retry
    Active --> [*]: Decommission
``` 
