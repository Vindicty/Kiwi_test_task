# Automated Testing Framework for Kiwi.com

This testing framework is designed to automate functional testing for the [Kiwi.com](https://www.kiwi.com/en/) web application. The framework is built using Python, Pytest, and Playwright, following the Page Object Model (POM) design pattern.

## Objectives
- **Ensure test reliability**: By isolating test logic from UI interactions, the framework minimizes maintenance efforts and enhances stability.
- **Simplify test management**: Tests are organized to allow for modularity and easy scalability.
- **Support CI/CD integration**: The framework is optimized for automated execution in a CI/CD environment, enabling continuous feedback on code quality.
- **Enable selective test execution**: Using Pytest markers, tests can be run individually or in groups based on tags.

## Key Features
1. **Page Object Model (POM)**: Encapsulation of UI elements and actions within reusable page classes.
2. **Integration with Pytest**: Simplifies test execution and reporting.
3. **Playwright for UI Automation**: Provides cross-browser support and reliable interaction with web elements.
4. **Dynamic Test Management**: YAML-based configuration allows dynamic test selection and execution in CI/CD pipelines.

## Project Architecture
The framework is organized into several key components, each serving a specific purpose. Below is a detailed description of the project structure:

### Key Directories and Their Purpose

1. **`.github/`**
   - Contains configurations for CI/CD pipelines.
   - **`tests_pipelines/`**: 
     - YAML files for dynamic test execution. These files define:
       - `BASIC_PATH`: Base directory for the test.
       - `TEST_PATH`: Path to the specific test file.
       - `REQUIREMENTS_PATH`: Path to the dependencies for the test.
     - Example: `basic_search.yml` defines the configuration for the basic search test.
   - **`workflows/`**:
     - Includes `ci.yml`, which defines the GitHub Actions pipeline for automated testing.

2. **`config/`**
   - Stores configuration files and utilities:
     - **`urls.py`**: Contains URLs used across the framework for easy management and reuse.

3. **`pages/`**
   - Implements the Page Object Model (POM) design pattern.
   - Each file represents a web page and encapsulates its elements and interactions.
     - **`home_page.py`**: Defines methods and locators for the homepage.
     - **`calendar_page.py`**: Handles interactions with the calendar functionality.

4. **`tests/`**
   - Main directory for all test cases and related files.
   - **`basic_search/`**:
     - **`test_basic_search.py`**: The test script for the basic search feature.
     - **`requirements.txt`**: Lists dependencies specific to this test.
   - **`features/`**:
     - **`basic_actions.feature`**: The Gherkin feature file defining the test scenarios.
   - **`step_definitions/`**:
     - **`home_steps.py`**: Contains step definitions for the Gherkin scenarios, implementing the actions and assertions.

5. **Root-Level Configuration Files**
   - **`.gitignore`**: Specifies files and directories to be ignored by Git.
   - **`conftest.py`**: Centralized fixture definitions for Pytest.
   - **`pytest.ini`**: Configuration file for Pytest, defining markers and other settings.

---

### Summary of Architectural Design
1. **Modularity**:
   - Each feature or functionality is isolated into its own directory, making the framework easy to maintain and scale.

2. **Reusability**:
   - The Page Object Model (POM) ensures that UI elements and actions can be reused across multiple tests.

3. **Scalability**:
   - Dynamic test pipelines and modular test design allow for easy addition of new tests and features.

4. **CI/CD Integration**:
   - The `ci.yml` workflow ensures seamless execution of tests in a CI/CD environment, supporting dynamic test discovery.

This architecture provides a solid foundation for functional UI testing while maintaining flexibility for future enhancements.

## How to Run Tests Locally

While tests are designed to run automatically via GitHub Actions, you can also execute them locally if needed. Below are the steps to set up and run the tests:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Vindicty/Kiwi_test_task.git
   cd Kiwi_test_task

2. **Install dependencies**:
    ```bash
    pip install -r tests/basic_search/requirements.txt

3. **Run the tests**:
   - ***To run all tests***:
     ```bash
     pytest
     ```
   - ***To run a specific test or group of tests***:
     ```bash
     pytest -m basic_search
     ```
     
### Notes

- **Dynamic Test Selection**:  
  Tests are configured to run dynamically using the YAML configurations located in `.github/tests_pipelines/`.

- **Page Object Model (POM)**:  
  This framework uses the POM design pattern to encapsulate web interactions, making it easier to write and maintain tests.

- **CI/CD**:  
  For automated test execution, tests are integrated into GitHub Actions via the `.github/workflows/ci.yml` configuration.


## Continuous Integration and Test Logs

This project uses **GitHub Actions** for continuous integration to automate test execution. The CI/CD pipeline is configured to:
- Install dependencies.
- Dynamically run tests based on the configurations provided in `.github/tests_pipelines/`.
- Generate logs for each workflow execution.

### How to View GitHub Actions Logs
You can view the logs of the automated tests directly in this repository:
1. Go to the [Actions tab](https://github.com/Vindicty/Kiwi_test_task/actions).
2. Select the latest workflow run (e.g., "CI Pipeline").
3. Click on the workflow run to expand the logs.
4. Navigate to specific sections (e.g., "Run tests") to see detailed execution logs.

### Example Workflow
Below is an example of the workflow process:
- **Environment Setup**: Installing dependencies and preparing the test environment.
- **Test Execution**: Running the test suite with `pytest` and generating logs.
- **Results**: Logs include detailed information about passed and failed tests.

By following the above steps, you can verify that the tests are correctly executed and analyze any potential issues directly from the logs.
