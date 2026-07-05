import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';

const products = defineCollection({
	loader: glob({ base: './src/content/products', pattern: '**/*.{md,mdx}' }),
	schema: z.object({
		title: z.string().min(1),
		brand: z.string().min(1),
		sku: z.string().optional(),
		category: z.string().optional(),
		image: z.string().min(1),
		images: z.array(z.string().min(1)).optional(),
		in_stock: z.boolean(),
		source_id: z.string().optional(),
		excerpt: z.string().optional(),
	}),
});

export const collections = { products };
