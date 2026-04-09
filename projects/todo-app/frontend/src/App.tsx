import { DarkModeToggle } from "./components/DarkModeToggle"
import { TaskForm } from "./components/TaskForm"
import { TaskList } from "./components/TaskList"
import { useDarkMode } from "./hooks/useDarkMode"
import { useTasks } from "./hooks/useTasks"
import "./App.css"

export function App() {
  const { tasks, loading, error, addTask, markDone, removeTask } = useTasks()
  const { isDark, toggle } = useDarkMode()

  return (
    <div className="app">
      <header className="app-header">
        <h1>Todo App</h1>
        <DarkModeToggle isDark={isDark} onToggle={toggle} />
      </header>
      <TaskForm onSubmit={addTask} />
      <TaskList
        tasks={tasks}
        loading={loading}
        error={error}
        onMarkDone={markDone}
        onDelete={removeTask}
      />
    </div>
  )
}
