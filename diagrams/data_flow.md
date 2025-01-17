# Data Flow Diagrams

## Device Registration Flow

```mermaid
flowchart TD
    subgraph Input
        D[Device]
        A[Admin]
    end

    subgraph Processing
        V[Validation Service]
        KG[Key Generation]
        R[Registration Service]
    end

    subgraph Storage
        DB[(Database)]
        KV[Key Vault]
    end

    D -->|Device Info| V
    A -->|Approval| V
    V -->|Validated Info| KG
    KG -->|Generated Keys| R
    KG -->|Store Keys| KV
    R -->|Store Device Info| DB
```

## Authentication Data Flow

```mermaid
flowchart LR
    subgraph External
        D[Device]
        R[Router]
    end

    subgraph Processing
        Auth[Auth Service]
        Val[Validation]
        KM[Key Manager]
    end

    subgraph Storage
        Cache[(Redis Cache)]
        DB[(PostgreSQL)]
        YK[YubiKey HSM]
    end

    D -->|Auth Request| R
    R -->|Forward Request| Auth
    Auth -->|Check Cache| Cache
    Auth -->|Validate Keys| Val
    Val -->|Verify| YK
    Val -->|Log| DB
    Auth -->|Get Keys| KM
    KM -->|Retrieve| YK
```

## Monitoring Data Flow

```mermaid
flowchart TB
    subgraph Sources
        YN[YubiKey Network]
        YM[YubiKey Monitor]
        Sys[System Metrics]
    end

    subgraph Collection
        C[Collector Service]
        P[Prometheus]
        G[Grafana]
    end

    subgraph Storage
        TS[(Time Series DB)]
        Log[(Log Storage)]
    end

    subgraph Alerts
        AM[Alert Manager]
        N[Notifications]
    end

    YN -->|Metrics| C
    YM -->|Status| C
    Sys -->|System Data| C
    C -->|Store| TS
    C -->|Store| Log
    TS --> P
    P --> G
    P --> AM
    AM --> N
```

## Key Management Data Flow

```mermaid
flowchart TD
    subgraph Input
        A[Admin]
        S[System]
    end

    subgraph Key Operations
        KG[Key Generation]
        KR[Key Rotation]
        KD[Key Distribution]
    end

    subgraph Storage
        YK[YubiKey HSM]
        KV[Key Vault]
        DB[(Database)]
    end

    subgraph Audit
        L[Logger]
        M[Monitor]
    end

    A -->|Request| KG
    S -->|Auto Rotation| KR
    KG -->|Generate| YK
    KR -->|Rotate| YK
    YK -->|Store| KV
    KD -->|Retrieve| KV
    KD -->|Metadata| DB
    KG -->|Log| L
    KR -->|Log| L
    L -->|Alert| M
```

## Backup Data Flow

```mermaid
flowchart TD
    subgraph Trigger
        S[Schedule]
        M[Manual]
    end

    subgraph Backup Process
        BP[Backup Processor]
        EC[Encryption]
        CP[Compression]
    end

    subgraph Sources
        DB[(Database)]
        KV[Key Vault]
        CF[Config Files]
    end

    subgraph Storage
        Local[Local Storage]
        Remote[Remote Storage]
    end

    S -->|Initiate| BP
    M -->|Initiate| BP
    BP -->|Read| DB
    BP -->|Read| KV
    BP -->|Read| CF
    BP -->|Process| EC
    EC -->|Compress| CP
    CP -->|Store| Local
    CP -->|Replicate| Remote
```

## Error Handling Flow

```mermaid
flowchart LR
    subgraph Sources
        App[Application]
        Sys[System]
        Net[Network]
    end

    subgraph Processing
        EH[Error Handler]
        Val[Validator]
        Rec[Recovery]
    end

    subgraph Actions
        Log[Logger]
        Alert[Alerts]
        Auto[Auto Recovery]
    end

    App -->|Error| EH
    Sys -->|Error| EH
    Net -->|Error| EH
    EH -->|Validate| Val
    Val -->|Process| Rec
    Rec -->|Write| Log
    Rec -->|Notify| Alert
    Rec -->|Fix| Auto
```

## Configuration Data Flow

```mermaid
flowchart TD
    subgraph Sources
        CF[Config Files]
        ENV[Environment]
        CMD[Command Line]
    end

    subgraph Processing
        CP[Config Processor]
        Val[Validator]
        Merge[Merger]
    end

    subgraph Distribution
        Cache[(Redis Cache)]
        Svcs[Services]
    end

    CF -->|Read| CP
    ENV -->|Read| CP
    CMD -->|Read| CP
    CP -->|Validate| Val
    Val -->|Combine| Merge
    Merge -->|Store| Cache
    Merge -->|Update| Svcs
```

## Audit Trail Flow

```mermaid
flowchart LR
    subgraph Events
        Auth[Authentication]
        Key[Key Operations]
        Sys[System Changes]
    end

    subgraph Processing
        Col[Collector]
        Val[Validator]
        Enc[Encryptor]
    end

    subgraph Storage
        DB[(Database)]
        Log[(Log Files)]
    end

    subgraph Analysis
        Rep[Reports]
        Alert[Alerts]
    end

    Auth -->|Event| Col
    Key -->|Event| Col
    Sys -->|Event| Col
    Col -->|Validate| Val
    Val -->|Encrypt| Enc
    Enc -->|Store| DB
    Enc -->|Write| Log
    DB -->|Generate| Rep
    Log -->|Monitor| Alert
``` 