# Image-Sequence Canvas Animation (on-demand reference)

The gold standard for scroll-driven animation (used by Apple, Stripe, Linear):

1. **Convert video to frame sequence** using FFmpeg
2. **Preload all frames** into memory as Image objects
3. **Draw frames to canvas** based on scroll position
4. **Use GSAP ScrollTrigger** for orchestration

### FFmpeg Video → Frames

```bash
# Extract 30fps frames as JPG (quality 2-5 for web)
ffmpeg -i input.mp4 -vf fps=30 -q:v 3 frames/frame_%04d.jpg

# Extract at lower fps for fewer frames (e.g., 15fps)
ffmpeg -i input.mp4 -vf fps=15 -q:v 3 frames/frame_%04d.jpg

# Create sprite sheet grid (10 columns)
ffmpeg -i input.mp4 -vf "fps=15,tile=10x10:padding=0" sprite_sheet.png
```

### Canvas Frame Animation Component (React)

```jsx
import { useRef, useEffect, useState } from 'react'
import { useGSAP } from '@gsap/react'
import gsap from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'

gsap.registerPlugin(ScrollTrigger)

export default function CanvasFrameAnimation({
  frameCount,
  framePath, // e.g., '/frames/hero/frame_%04d.jpg'
  width = 1920,
  height = 1080,
  scrollTriggerRef, // ref to the scroll container
}) {
  const canvasRef = useRef(null)
  const imagesRef = useRef([])
  const [loaded, setLoaded] = useState(0)

  // Preload all frames
  useEffect(() => {
    const images = []
    let loadedCount = 0

    for (let i = 1; i <= frameCount; i++) {
      const img = new Image()
      const src = framePath.replace('%04d', String(i).padStart(4, '0'))
      img.src = src
      img.onload = () => {
        loadedCount++
        setLoaded(loadedCount)
      }
      images.push(img)
    }
    imagesRef.current = images
  }, [frameCount, framePath])

  // Draw frames on scroll
  useGSAP(() => {
    if (!canvasRef.current || loaded < frameCount) return
    const ctx = canvasRef.current.getContext('2d')
    const canvas = canvasRef.current

    ScrollTrigger.create({
      trigger: scrollTriggerRef?.current || canvas,
      start: 'top top',
      end: 'bottom bottom',
      scrub: 0.5,
      onUpdate: (self) => {
        const frameIndex = Math.min(
          frameCount - 1,
          Math.floor(self.progress * frameCount)
        )
        const img = imagesRef.current[frameIndex]
        if (img && img.complete) {
          ctx.clearRect(0, 0, canvas.width, canvas.height)
          ctx.drawImage(img, 0, 0, canvas.width, canvas.height)
        }
      },
    })
  }, { scope: scrollTriggerRef })

  return (
    <canvas
      ref={canvasRef}
      width={width}
      height={height}
      style={{
        position: 'sticky',
        top: 0,
        width: '100%',
        height: '100vh',
        objectFit: 'cover',
      }}
    />
  )
}
```
