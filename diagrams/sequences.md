# Sequence Diagrams

## Device Registration Sequence

```mermaid
sequenceDiagram
    participant D as Device
    participant R as Router
    participant API as API Server
    participant Auth as Auth Service
    participant YK as YubiKey HSM
    participant DB as Database
    participant Admin as Administrator

    D->>R: Submit Registration Request
    R->>API: Forward Registration
    API->>Auth: Validate Request
    Auth->>DB: Check Device Status
    DB-->>Auth: Device Not Registered
    Auth->>Admin: Request Approval
    Admin-->>Auth: Approve Registration
    Auth->>YK: Generate Device Keys
    YK-->>Auth: Keys Generated
    Auth->>DB: Store Device Info
    Auth-->>API: Registration Complete
    API-->>R: Send Credentials
    R-->>D: Registration Successful
```

## Authentication Sequence

```mermaid
sequenceDiagram
    participant D as Device
    participant R as Router
    participant API as API Server
    participant Cache as Redis Cache
    participant Auth as Auth Service
    participant YK as YubiKey HSM
    participant DB as Database

    D->>R: Authentication Request
    R->>API: Forward Auth Request
    API->>Cache: Check Session
    Cache-->>API: No Active Session
    API->>Auth: Validate Credentials
    Auth->>YK: Verify Device Key
    YK-->>Auth: Key Verified
    Auth->>DB: Log Authentication
    Auth-->>API: Auth Successful
    API->>Cache: Store Session
    API-->>R: Send Auth Token
    R-->>D: Connection Established
```

## Key Rotation Sequence

```mermaid
sequenceDiagram
    participant Sys as System
    participant KM as Key Manager
    participant YK as YubiKey HSM
    participant DB as Database
    participant Cache as Redis Cache
    participant Log as Logger
    participant Alert as Alert System

    Sys->>KM: Initiate Key Rotation
    KM->>DB: Check Key Status
    DB-->>KM: Key Age Verified
    KM->>YK: Generate New Key
    YK-->>KM: New Key Generated
    KM->>DB: Store New Key Metadata
    KM->>Cache: Update Key Cache
    KM->>Log: Record Key Rotation
    Log->>Alert: Notify Admin
    KM->>YK: Revoke Old Key
    YK-->>KM: Key Revoked
    KM->>DB: Update Key Status
    KM-->>Sys: Rotation Complete
```

## Backup Process Sequence

```mermaid
sequenceDiagram
    participant Sys as System
    participant BP as Backup Process
    participant DB as Database
    participant YK as YubiKey HSM
    participant FS as File System
    participant Enc as Encryption
    participant RS as Remote Storage
    participant Log as Logger

    Sys->>BP: Initiate Backup
    BP->>DB: Export Database
    DB-->>BP: Database Dump
    BP->>YK: Export Keys
    YK-->>BP: Key Export
    BP->>FS: Read Config Files
    FS-->>BP: Config Data
    BP->>Enc: Encrypt Backup
    Enc-->>BP: Encrypted Data
    BP->>FS: Store Local Backup
    BP->>RS: Replicate Backup
    RS-->>BP: Replication Complete
    BP->>Log: Record Backup
    BP-->>Sys: Backup Complete
```

## Error Recovery Sequence

```mermaid
sequenceDiagram
    participant Sys as System
    participant EH as Error Handler
    participant Val as Validator
    participant Rec as Recovery
    participant DB as Database
    participant YK as YubiKey HSM
    participant Log as Logger
    participant Alert as Alert System

    Sys->>EH: Error Detected
    EH->>Val: Validate Error
    Val->>DB: Check System State
    DB-->>Val: State Retrieved
    Val->>YK: Verify Keys
    YK-->>Val: Key Status
    Val-->>EH: Error Validated
    EH->>Rec: Initiate Recovery
    Rec->>DB: Restore State
    Rec->>YK: Reset Keys
    Rec->>Log: Record Recovery
    Log->>Alert: Notify Admin
    Rec-->>EH: Recovery Complete
    EH-->>Sys: Error Resolved
```

## Monitoring Sequence

```mermaid
sequenceDiagram
    participant Sys as System
    participant Mon as Monitor
    participant Met as Metrics
    participant DB as Database
    participant P as Prometheus
    participant G as Grafana
    participant Alert as Alert Manager
    participant Admin as Administrator

    Sys->>Mon: Generate Metrics
    Mon->>Met: Collect Data
    Met->>DB: Store Metrics
    Met->>P: Update Prometheus
    P->>G: Update Dashboard
    P->>Alert: Check Thresholds
    Alert->>Admin: Send Alert
    Mon->>DB: Log Status
    Mon-->>Sys: Monitoring Complete
```

## Configuration Update Sequence

```mermaid
sequenceDiagram
    participant Admin as Administrator
    participant CM as Config Manager
    participant Val as Validator
    participant DB as Database
    participant Cache as Redis Cache
    participant Svc as Services
    participant Log as Logger

    Admin->>CM: Update Config
    CM->>Val: Validate Changes
    Val->>DB: Check Dependencies
    DB-->>Val: Dependencies OK
    Val-->>CM: Changes Valid
    CM->>DB: Store New Config
    CM->>Cache: Update Cache
    CM->>Svc: Notify Services
    Svc-->>CM: Config Applied
    CM->>Log: Record Changes
    CM-->>Admin: Update Complete
```

## Audit Trail Sequence

```mermaid
sequenceDiagram
    participant Sys as System
    participant AT as Audit Trail
    participant Val as Validator
    participant Enc as Encryptor
    participant DB as Database
    participant Log as Logger
    participant Rep as Reporter
    participant Admin as Administrator

    Sys->>AT: Generate Event
    AT->>Val: Validate Event
    Val->>Enc: Encrypt Data
    Enc->>DB: Store Event
    Enc->>Log: Write Log
    Admin->>Rep: Request Report
    Rep->>DB: Query Events
    DB-->>Rep: Event Data
    Rep->>Enc: Decrypt Data
    Enc-->>Rep: Readable Data
    Rep-->>Admin: Generate Report
``` 