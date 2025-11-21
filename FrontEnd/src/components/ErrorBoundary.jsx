import React from "react";

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      hasError: false,
      error: null,
      errorInfo: null,
    };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    console.error("Error caught by ErrorBoundary:", error, errorInfo);
    this.setState({ errorInfo });
  }

  resetError = () => {
    this.setState({ hasError: false, error: null, errorInfo: null });
  };

  render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-screen bg-gradient-to-br from-red-50 to-red-100 p-6 flex items-center justify-center">
          <div className="bg-white rounded-lg shadow-xl p-8 max-w-md">
            <div className="text-center">
              <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-red-100 mb-4">
                <span className="text-2xl">⚠️</span>
              </div>
              <h1 className="text-2xl font-bold text-red-700 mb-2">
                Oops! Something Went Wrong
              </h1>
              <p className="text-gray-600 mb-4">
                We're sorry for the inconvenience. An unexpected error occurred.
              </p>
            </div>

            <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6 text-sm">
              <p className="font-mono text-red-700 break-words">
                {this.state.error?.message || "Unknown error"}
              </p>
            </div>

            {process.env.NODE_ENV === "development" && this.state.errorInfo && (
              <details className="mb-6 text-xs text-gray-600 bg-gray-50 p-3 rounded border border-gray-200">
                <summary className="cursor-pointer font-semibold mb-2">
                  Error Details (Dev)
                </summary>
                <pre className="overflow-auto max-h-32 text-red-700">
                  {this.state.errorInfo.componentStack}
                </pre>
              </details>
            )}

            <div className="space-y-2">
              <button
                onClick={this.resetError}
                className="w-full px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors font-medium"
              >
                Try Again
              </button>
              <button
                onClick={() => (window.location.href = "/")}
                className="w-full px-4 py-2 bg-gray-300 text-gray-800 rounded-lg hover:bg-gray-400 transition-colors font-medium"
              >
                Go to Home
              </button>
            </div>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;
