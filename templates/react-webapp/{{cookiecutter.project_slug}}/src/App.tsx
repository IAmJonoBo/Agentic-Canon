import './App.css';

const PROJECT_NAME = '{{ cookiecutter.project_name }}';
const PROJECT_DESCRIPTION = '{{ cookiecutter.description }}';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>{PROJECT_NAME}</h1>
        <p>{PROJECT_DESCRIPTION}</p>
        <p className="read-the-docs">
          Edit <code>src/App.tsx</code> and save to reload
        </p>
      </header>
    </div>
  );
}

export default App;
