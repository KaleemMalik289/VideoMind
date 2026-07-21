import React from "react"
import { motion } from "framer-motion"
import type { HTMLMotionProps } from "framer-motion"

export const FadeIn = React.forwardRef<HTMLDivElement, HTMLMotionProps<"div"> & { delay?: number }>(
  ({ children, delay = 0, ...props }, ref) => {
    return (
      <motion.div
        ref={ref}
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        transition={{ duration: 0.3, delay }}
        {...props}
      >
        {children}
      </motion.div>
    )
  }
)
FadeIn.displayName = "FadeIn"
