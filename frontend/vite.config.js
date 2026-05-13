import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve, dirname } from 'path'
import { cpSync, existsSync, createReadStream } from 'fs'
import { fileURLToPath } from 'url'

const __dirname = dirname(fileURLToPath(import.meta.url))

function imagesPlugin() {
  return {
    name: 'images-plugin',
    // Serve src/images/ at /images/ during development
    configureServer(server) {
      server.middlewares.use('/images', (req, res, next) => {
        const filePath = resolve(__dirname, 'src/images', req.url.replace(/^\//, ''))
        if (existsSync(filePath)) {
          createReadStream(filePath).pipe(res)
        } else {
          next()
        }
      })
    },
    // Copy src/images/ to dist/images/ after production build
    closeBundle() {
      const src = resolve(__dirname, 'src/images')
      const dest = resolve(__dirname, 'dist/images')
      if (existsSync(src)) {
        cpSync(src, dest, { recursive: true })
      }
    }
  }
}

export default defineConfig({
  plugins: [vue(), imagesPlugin()],
  server: {
    port: 5173,
    host: true
  }
})
