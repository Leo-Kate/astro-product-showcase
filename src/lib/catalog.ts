export const site = {
	name: 'Mirck',
	tagline: 'Richard Mille Private Catalogue',
	whatsappNumber: '19189225678',
	url: 'https://mirck.co',
};

export function slugify(value: string) {
	return value
		.toLowerCase()
		.replace(/['']/g, '')
		.replace(/[^a-z0-9]+/g, '-')
		.replace(/-{2,}/g, '-')
		.replace(/^-|-$/g, '') || 'collection';
}

export function collectionName(category?: string) {
	const parts = (category ?? '')
		.split('>')
		.map((part) => part.trim())
		.filter(Boolean);

	return parts.length > 1 ? parts[parts.length - 1] : parts[0] || 'Richard Mille';
}

export function collectionPath(category?: string) {
	return `/collections/${slugify(collectionName(category))}/`;
}

export function priceLabel(price?: number) {
	return typeof price === 'number'
		? new Intl.NumberFormat('en-US', {
				style: 'currency',
				currency: 'USD',
				maximumFractionDigits: 0,
			}).format(price)
		: 'Price on request';
}

export function whatsappHref(message: string) {
	if (!site.whatsappNumber) {
		return '';
	}

	return `https://wa.me/${site.whatsappNumber}?text=${encodeURIComponent(message)}`;
}

export function productInquiryHref(title: string, sku: string | undefined, path: string) {
	const details = [title, sku ? `SKU: ${sku}` : '', `${site.url}${path}`].filter(Boolean).join('\n');
	return whatsappHref(`Hi, I want to inquire about this Richard Mille piece:\n${details}`);
}

export function isAccessoryProduct(product: { data: { title: string; category?: string; sku?: string } }) {
	const value = `${product.data.title} ${product.data.category ?? ''} ${product.data.sku ?? ''}`.toLowerCase();
	return /\b(screw|box set|make up|difference|coupon|shipping|bezel|case back|accessor)/i.test(value);
}

export function compareProductsForDisplay(
	a: { data: { title: string; category?: string; sku?: string } },
	b: { data: { title: string; category?: string; sku?: string } },
) {
	const accessorySort = Number(isAccessoryProduct(a)) - Number(isAccessoryProduct(b));
	if (accessorySort !== 0) {
		return accessorySort;
	}

	return collectionName(a.data.category).localeCompare(collectionName(b.data.category)) || a.data.title.localeCompare(b.data.title);
}
