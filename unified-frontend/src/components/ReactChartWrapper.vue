<template>
  <div ref="reactContainer" class="react-chart-wrapper"></div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'
import { createRoot } from 'react-dom/client'
import * as React from 'react'

const props = defineProps({
  component: {
    type: Object,
    required: true
  },
  componentProps: {
    type: Object,
    default: () => ({})
  }
})

const reactContainer = ref(null)
let root = null

const renderReactComponent = () => {
  if (reactContainer.value) {
    // 清理之前的渲染
    if (root) {
      root.unmount()
    }
    
    // 创建新的React根并渲染
    root = createRoot(reactContainer.value)
    root.render(React.createElement(props.component, props.componentProps))
  }
}

onMounted(() => {
  renderReactComponent()
})

onUnmounted(() => {
  if (root) {
    root.unmount()
  }
})

watch(() => props.componentProps, () => {
  renderReactComponent()
}, { deep: true })
</script>

<style scoped>
.react-chart-wrapper {
  width: 100%;
  height: 100%;
}
</style>