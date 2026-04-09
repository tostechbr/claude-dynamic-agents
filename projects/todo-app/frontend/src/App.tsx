import { TaskForm } from "./components/TaskForm"
import { TaskList } from "./components/TaskList"
import { useTasks } from "./hooks/useTasks"
import "./App.css"

export function App() {
  const { tasks, loading, error, addTask, markDone, removeTask } = useTasks()

  return (
    <div className="app">
      <h1>Todo App</h1>
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
