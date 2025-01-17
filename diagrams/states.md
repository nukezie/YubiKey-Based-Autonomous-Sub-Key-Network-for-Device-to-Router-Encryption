# State Diagrams

## Device States

```mermaid
stateDiagram-v2
    [*] --> Unregistered
    Unregistered --> PendingApproval: Submit Registration
    PendingApproval --> Registered: Admin Approves
    PendingApproval --> Rejected: Admin Rejects
    Registered --> Active: Authentication Success
    Active --> Inactive: Session Timeout
    Inactive --> Active: Re-authenticate
    Active --> Suspended: Security Violation
    Suspended --> Active: Admin Reset
    Registered --> Decommissioned: Admin Decommission
    Decommissioned --> [*]
    Rejected --> Unregistered: Retry Registration
```

## Key Lifecycle States

```mermaid
stateDiagram-v2
    [*] --> Generated
    Generated --> Active: Activation
    Active --> Rotating: Scheduled Rotation
    Rotating --> Active: Rotation Complete
    Active --> Compromised: Security Alert
    Compromised --> Revoked: Emergency Response
    Active --> Expired: Time/Usage Limit
    Expired --> Archived: Backup
    Archived --> [*]
    Revoked --> Archived: Backup
    Active --> Suspended: Admin Action
    Suspended --> Active: Admin Reset
```

## Authentication Session States

```mermaid
stateDiagram-v2
    [*] --> Initial
    Initial --> Authenticating: Present Credentials
    Authenticating --> Validated: Verify Success
    Authenticating --> Failed: Verify Failed
    Failed --> Blocked: Max Attempts
    Failed --> Initial: Retry
    Validated --> Active: Session Created
    Active --> Refreshing: Token Expiring
    Refreshing --> Active: Token Renewed
    Refreshing --> Expired: Renewal Failed
    Active --> Expired: Timeout
    Expired --> Initial: Re-authenticate
    Blocked --> Initial: Admin Reset
    Active --> Terminated: Logout
    Terminated --> [*]
```

## Backup Process States

```mermaid
stateDiagram-v2
    [*] --> Idle
    Idle --> Preparing: Trigger Backup
    Preparing --> Collecting: Init Success
    Preparing --> Failed: Init Error
    Collecting --> Encrypting: Data Collected
    Encrypting --> Storing: Encryption Done
    Storing --> Replicating: Local Store Done
    Replicating --> Verifying: Replication Done
    Verifying --> Success: Verify Pass
    Verifying --> Failed: Verify Fail
    Success --> Idle: Cleanup Done
    Failed --> Idle: Cleanup Done
```

## Monitoring System States

```mermaid
stateDiagram-v2
    [*] --> Running
    Running --> Collecting: Schedule/Trigger
    Collecting --> Processing: Data Received
    Processing --> Alerting: Threshold Exceeded
    Processing --> Running: Normal Range
    Alerting --> Notifying: Alert Generated
    Notifying --> Running: Alert Sent
    Running --> Paused: Admin Action
    Paused --> Running: Resume
    Running --> Error: System Issue
    Error --> Running: Auto-recover
    Error --> Stopped: Critical Error
    Stopped --> [*]
```

## Configuration States

```mermaid
stateDiagram-v2
    state "Default" as s1
    state "Editing" as s2
    state "Validating" as s3
    state "Deploying" as s4
    state "Failed" as s5
    state "Active" as s6
    state "RollingBack" as s7
    state "Previous" as s8

    [*] --> s1
    s1 --> s2: Admin Modify
    s2 --> s3: Save Changes
    s3 --> s4: Validation Pass
    s3 --> s5: Validation Error
    s5 --> s2: Retry
    s4 --> s6: Deploy Success
    s4 --> s7: Deploy Error
    s7 --> s8: Rollback Success
    s8 --> s1: Reset
    s6 --> s8: Version Change
```

## Error Handling States

```mermaid
stateDiagram-v2
    [*] --> Normal
    Normal --> Detected: Error Occurs
    Detected --> Analyzing: Log Error
    Analyzing --> Minor: Low Severity
    Analyzing --> Major: High Severity
    Analyzing --> Critical: System Threat
    Minor --> Resolving: Auto-fix
    Major --> Alerting: Notify Admin
    Critical --> Emergency: Shutdown/Isolate
    Resolving --> Normal: Fix Applied
    Alerting --> Resolving: Admin Action
    Emergency --> Recovering: Crisis Managed
    Recovering --> Normal: System Restored
```

## Service Health States

```mermaid
stateDiagram-v2
    [*] --> Starting
    Starting --> Running: Init Success
    Starting --> Failed: Init Error
    Running --> Degraded: Performance Issue
    Degraded --> Running: Auto-recover
    Running --> Maintenance: Scheduled
    Maintenance --> Running: Complete
    Running --> Stopped: Admin Action
    Stopped --> Starting: Restart
    Failed --> Starting: Retry
    Running --> Failed: Critical Error
    Failed --> [*]: Unrecoverable
``` 
