import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';

const products = defineCollection({
	loader: glob({ base: './src/content/products', pattern: '**/*.{md,mdx}' }),
	schema: z.object({
		title: z.string().min(1),
		brand: z.string().min(1),
		image: z.string().startsWith('/'),
		price: z.number().nonnegative(),
		in_stock: z.boolean(),
	}),
});

export const collections = { products };
