import { ref } from 'vue'

const toasts = ref([])

export const useToast = () => {
  let id = 0

  const add = (message, type = 'info', duration = 3000) => {
    const toastId = id++
    const toast = {
      id: toastId,
      message,
      type
    }
    
    toasts.value.push(toast)

    if (duration > 0) {
      setTimeout(() => {
        remove(toastId)
      }, duration)
    }

    return toastId
  }

  const remove = (id) => {
    toasts.value = toasts.value.filter(t => t.id !== id)
  }

  return {
    toasts,
    success: (message) => add(message, 'success'),
    error: (message) => add(message, 'error', 5000),
    info: (message) => add(message, 'info'),
    warning: (message) => add(message, 'warning'),
    add,
    remove
  }
}
