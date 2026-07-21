import React from "react"
import { motion } from "framer-motion"
import type { HTMLMotionProps } from "framer-motion"

export const SlideIn = React.forwardRef<HTMLDivElement, HTMLMotionProps<"div"> & { direction?: "up" | "down" | "left" | "right", delay?: number }>(
  ({ children, direction = "up", delay = 0, ...props }, ref) => {
    
    const variants = {
      hidden: {
        opacity: 0,
        y: direction === "up" ? 20 : direction === "down" ? -20 : 0,
        x: direction === "left" ? 20 : direction === "right" ? -20 : 0,
      },
      visible: {
        opacity: 1,
        y: 0,
        x: 0,
      }
    }

    return (
      <motion.div
        ref={ref}
        initial="hidden"
        animate="visible"
        exit="hidden"
        variants={variants}
        transition={{ duration: 0.4, delay, ease: "easeOut" }}
        {...props}
      >
        {children}
      </motion.div>
    )
  }
)
SlideIn.displayName = "SlideIn"
