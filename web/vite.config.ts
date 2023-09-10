import {defineConfig} from 'vite'
import react from '@vitejs/plugin-react-swc'
import {VitePWA} from 'vite-plugin-pwa'

// https://vitejs.dev/config/
export default defineConfig({
    plugins: [react(), VitePWA({
        registerType: 'autoUpdate', devOptions: {
            enabled: true
        }, manifest: {
            name: 'GovernMental Hacks',
            short_name: 'GovernMental',
            start_url: '.',
            display: 'standalone',
            theme_color: '#ffffff',
        }
    })],
})
