---
name: react-patterns
description: "Use when building or reviewing React frontends: component architecture, hooks, TypeScript patterns, state management, file structure"
---

# React Patterns

## Project Structure

```
src/
├── app/                 ← routing, layouts (Next.js app router or React Router)
├── components/
│   ├── ui/              ← generic, reusable (Button, Input, Modal)
│   └── features/        ← feature-specific (AuthForm, UserCard)
├── hooks/               ← custom hooks
├── services/            ← API calls (no fetch in components)
├── stores/              ← global state (Zustand / Jotai)
├── types/               ← shared TypeScript types
└── utils/               ← pure utility functions
```

## Component Patterns

```tsx
// Prefer named exports for components
export function UserCard({ user, onEdit }: UserCardProps) {
  return (...)
}

// Types defined above the component, not inline
interface UserCardProps {
  user: User
  onEdit: (id: string) => void
}
```

## Custom Hooks

Extract logic from components into hooks:

```tsx
// hooks/useAuth.ts
export function useAuth() {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    authService.getMe()
      .then(setUser)
      .finally(() => setLoading(false))
  }, [])

  return { user, loading, isAuthenticated: !!user }
}

// Usage — component stays clean
export function Header() {
  const { user, isAuthenticated } = useAuth()
  return isAuthenticated ? <UserMenu user={user!} /> : <LoginButton />
}
```

## Data Fetching (TanStack Query)

```tsx
// services/users.ts — API calls isolated here
export const usersService = {
  getById: (id: string) =>
    fetch(`/api/users/${id}`).then(r => r.json()),
}

// hooks/useUser.ts
export function useUser(id: string) {
  return useQuery({
    queryKey: ["users", id],
    queryFn: () => usersService.getById(id),
  })
}

// Component stays simple
export function UserPage({ id }: { id: string }) {
  const { data: user, isPending, error } = useUser(id)

  if (isPending) return <Spinner />
  if (error) return <ErrorMessage error={error} />
  return <UserCard user={user} />
}
```

## State Management (Zustand)

```tsx
// stores/authStore.ts
import { create } from "zustand"

interface AuthStore {
  user: User | null
  setUser: (user: User | null) => void
}

export const useAuthStore = create<AuthStore>((set) => ({
  user: null,
  setUser: (user) => set({ user }),
}))
```

## Form Handling (React Hook Form)

```tsx
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { z } from "zod"

const schema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
})

type FormData = z.infer<typeof schema>

export function LoginForm({ onSuccess }: { onSuccess: () => void }) {
  const { register, handleSubmit, formState: { errors } } = useForm<FormData>({
    resolver: zodResolver(schema),
  })

  const onSubmit = async (data: FormData) => {
    await authService.login(data)
    onSuccess()
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register("email")} />
      {errors.email && <span>{errors.email.message}</span>}
    </form>
  )
}
```

## Key Principles

- Components are responsible for rendering, not for data fetching or business logic
- Custom hooks own all stateful and async logic
- Services own all API calls — never call `fetch` directly in a component
- Use TypeScript strictly — no `any`
- Co-locate: test file next to component (`UserCard.test.tsx`)
- Prefer composition over prop drilling — use Context or Zustand for deep state
