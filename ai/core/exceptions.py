class PortfolioAutomationError(Exception):
    """Base error for the portfolio automation platform."""


class ConfigurationError(PortfolioAutomationError):
    """Raised when required configuration is absent or invalid."""


class ProviderError(PortfolioAutomationError):
    """Raised when an LLM provider cannot complete a request."""


class EvidenceValidationError(PortfolioAutomationError):
    """Raised when an artifact contains unsupported factual claims."""


class AgentExecutionError(PortfolioAutomationError):
    """Raised when an agent cannot finish its responsibility."""


class FileChangeValidationError(PortfolioAutomationError):
    """Raised when a proposed file change violates execution policies."""
