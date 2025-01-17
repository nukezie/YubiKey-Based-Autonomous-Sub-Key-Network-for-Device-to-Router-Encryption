# YubiKey Network System Diagrams

This directory contains comprehensive diagrams documenting the architecture, flows, and states of the YubiKey-Based Autonomous Sub-Key Network system. All diagrams are written in Mermaid markdown format for easy version control and rendering.

## Diagram Types

### Architecture Diagrams (`architecture.md`)
- **High-Level Architecture**: Overall system structure showing all major components and their relationships
- **Key Management Flow**: Key generation and distribution architecture
- **Monitoring Architecture**: System monitoring and alerting setup
- **Backup and Recovery Flow**: Backup system architecture
- **Deployment Architecture**: System deployment structure
- **Authentication Flow**: Authentication system architecture
- **Network Topology**: Physical and logical network layout
- **Key Rotation Process**: Key lifecycle management architecture

### Data Flow Diagrams (`data_flow.md`)
- **Device Registration Flow**: Data movement during device registration
- **Authentication Data Flow**: Data flow during authentication process
- **Monitoring Data Flow**: Metrics and monitoring data movement
- **Key Management Data Flow**: Key-related data handling
- **Backup Data Flow**: Data movement during backup operations
- **Error Handling Flow**: Error detection and recovery data flow
- **Configuration Data Flow**: Configuration management flow
- **Audit Trail Flow**: Audit logging and reporting data flow

### Sequence Diagrams (`sequences.md`)
- **Device Registration Sequence**: Step-by-step device registration process
- **Authentication Sequence**: Detailed authentication steps
- **Key Rotation Sequence**: Key rotation procedure
- **Backup Process Sequence**: Backup operation steps
- **Error Recovery Sequence**: Error handling procedure
- **Monitoring Sequence**: System monitoring process
- **Configuration Update Sequence**: Configuration change process
- **Audit Trail Sequence**: Audit logging procedure

### State Diagrams (`states.md`)
- **Device States**: Possible device states and transitions
- **Key Lifecycle States**: Key states throughout their lifecycle
- **Authentication Session States**: Session state transitions
- **Backup Process States**: States during backup operations
- **Monitoring System States**: Monitoring service states
- **Configuration States**: Configuration management states
- **Error Handling States**: Error processing states
- **Service Health States**: Service lifecycle states

## Usage

These diagrams serve multiple purposes:
1. **Documentation**: Comprehensive system documentation
2. **Development Reference**: Guide for implementing features
3. **Troubleshooting**: Understanding system behavior
4. **Training**: Onboarding new team members
5. **Architecture Planning**: Planning system changes

## Viewing the Diagrams

The diagrams can be viewed in several ways:
1. **GitHub**: Directly rendered in GitHub's markdown viewer
2. **Mermaid Live Editor**: Copy diagram code to [Mermaid Live Editor](https://mermaid.live)
3. **Documentation Tools**: Any documentation system supporting Mermaid
4. **IDE Plugins**: Various IDE plugins that render Mermaid diagrams

## Maintaining the Diagrams

When updating the system, please:
1. Keep diagrams in sync with code changes
2. Maintain consistent styling across diagrams
3. Update relevant diagrams when adding features
4. Include diagram updates in pull requests
5. Validate diagram syntax before committing

## Contributing

When contributing new diagrams or updates:
1. Follow the established naming conventions
2. Use consistent styling and formatting
3. Include clear labels and descriptions
4. Test diagram rendering before submitting
5. Update this README when adding new diagram types

## Best Practices

1. **Clarity**: Keep diagrams clear and readable
2. **Consistency**: Use consistent notation
3. **Completeness**: Include all relevant components
4. **Accuracy**: Keep diagrams in sync with implementation
5. **Documentation**: Include explanatory notes

## Tools and Resources

- [Mermaid Documentation](https://mermaid-js.github.io/mermaid/)
- [Mermaid Live Editor](https://mermaid.live)
- [GitHub Mermaid Support](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/creating-diagrams)
- [VS Code Mermaid Extension](https://marketplace.visualstudio.com/items?itemName=bierner.markdown-mermaid) 