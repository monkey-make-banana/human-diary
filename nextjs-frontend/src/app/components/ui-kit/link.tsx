/**
 * TODO: Update this component to use your client-side framework's link
 * component. We've provided examples of how to do this for Next.js, Remix, and
 * Inertia.js in the Catalyst documentation:
 *
 * https://catalyst.tailwindui.com/docs#client-side-router-integration
 */

import NextLink, { type LinkProps as NextLinkProps } from 'next/link'
import React, { forwardRef } from 'react'

type AnchorProps = Omit<React.ComponentPropsWithoutRef<'a'>, keyof NextLinkProps>

export const Link = forwardRef<HTMLAnchorElement, NextLinkProps & AnchorProps>(function Link(props, ref) {
  return <NextLink {...props} ref={ref} />
})
