/**
 * AL MAJD — Product Catalog
 * Edit this file to add/update/remove products
 *
 * Categories: "oud" | "attar" | "bakhoor" | "rose"
 * badge: optional — "Novo" | "Exclusivo" | "Best Seller" | "Edição Limitada"
 */

const PRODUCTS = [
  {
    id: "oud-al-qamari",
    name: "Oud Al Qamari",
    category: "oud",
    volume: "12ml",
    price: 89,
    oldPrice: null,
    badge: "Best Seller",
    icon: "🌙",
    shortNotes: "Oud escuro · Âmbar · Sândalo",
    description: "Uma ode ao oud mais puro do Bangladesh. Notas profundas e terrosas de agarwood envoltas em sândalo cremoso e âmbar dourado. Uma fragrância que dura mais de 12 horas na pele.",
    notes: {
      topo: "Oud Bengali, Especiarias",
      meio: "Sândalo, Rosa Negra",
      base: "Âmbar, Almíscar, Balsâmico"
    },
    tags: ["oud", "intenso", "unissexo"]
  },
  {
    id: "royal-rose-attar",
    name: "Royal Rose Attar",
    category: "attar",
    volume: "10ml",
    price: 65,
    oldPrice: null,
    badge: "Exclusivo",
    icon: "🌹",
    shortNotes: "Rosa de Taif · Oud · Almizcle",
    description: "A rosa mais rara do mundo árabe, colhida ao amanhecer nas montanhas de Taif. Um attar puro sem álcool que se funde com a sua pele e cria uma fragrância única, pessoal e inesquecível.",
    notes: {
      topo: "Rosa de Taif, Bergamota",
      meio: "Oud, Geranio, Jasmim",
      base: "Almíscar Branco, Baunilha"
    },
    tags: ["attar", "floral", "unissexo"]
  },
  {
    id: "musk-al-sultan",
    name: "Musk Al Sultan",
    category: "attar",
    volume: "10ml",
    price: 55,
    oldPrice: 70,
    badge: null,
    icon: "✦",
    shortNotes: "Almíscar Branco · Âmbar · Baunilha",
    description: "O almíscar dos palácios do Golfo. Limpo, sensual e envolvente — ideal para quem procura uma fragrância discreta mas marcante. Perfeito para o dia a dia e para ocasiões especiais.",
    notes: {
      topo: "Almíscar Branco, Aldeídos",
      meio: "Âmbar Cinza, Cedro",
      base: "Baunilha, Madeira de Caxemira"
    },
    tags: ["attar", "limpo", "unissexo"]
  },
  {
    id: "oudh-cambodi-noir",
    name: "Oudh Cambodi Noir",
    category: "oud",
    volume: "3ml",
    price: 120,
    oldPrice: null,
    badge: "Edição Limitada",
    icon: "◆",
    shortNotes: "Oud Camboja · Defumado · Terroso",
    description: "O oud mais raro da nossa coleção. Proveniente de árvores centenárias do Camboja, este óleo puro tem uma complexidade que só se desenvolve ao longo de horas na sua pele. Para os verdadeiros apreciadores.",
    notes: {
      topo: "Oud Camboja Puro",
      meio: "Especiarias Negras, Tabaco",
      base: "Terra, Musgo, Resina"
    },
    tags: ["oud", "raro", "unissexo"]
  },
  {
    id: "bakhoor-al-oud",
    name: "Bakhoor Al Oud",
    category: "bakhoor",
    volume: "50g",
    price: 38,
    oldPrice: null,
    badge: "Novo",
    icon: "〰",
    shortNotes: "Incenso Árabe · Oud · Sândalo",
    description: "Fragmentos de madeira de oud embebidos em óleos essenciais preciosos. Queime sobre carvão ou numa mabkhara elétrica para perfumar toda a sua casa com o aroma autêntico das casas árabes de luxo.",
    notes: {
      topo: "Fumo de Oud, Sândalo",
      meio: "Rosa, Canela, Cravo",
      base: "Âmbar, Resina de Bálsamo"
    },
    tags: ["bakhoor", "casa", "incenso"]
  },
  {
    id: "amber-al-sharq",
    name: "Amber Al Sharq",
    category: "attar",
    volume: "12ml",
    price: 72,
    oldPrice: null,
    badge: null,
    icon: "◉",
    shortNotes: "Âmbar Dourado · Oud · Especiarias",
    description: "Uma viagem ao coração do Médio Oriente. Âmbar dourado quente e rico, abraçado por oud e um bouquet de especiarias exóticas. Ideal para noites de inverno e ocasiões especiais.",
    notes: {
      topo: "Âmbar Dourado, Açafrão",
      meio: "Oud, Rosa, Patchouli",
      base: "Benjoim, Almíscar, Âmbar Cinza"
    },
    tags: ["attar", "quente", "unissexo"]
  },
  {
    id: "white-oud-medina",
    name: "White Oud Medina",
    category: "oud",
    volume: "12ml",
    price: 95,
    oldPrice: null,
    badge: null,
    icon: "○",
    shortNotes: "Oud Branco · Floral · Almíscar",
    description: "A versão mais luminosa e etérea do oud. Proveniente das regiões mais frescas da Arábia, este oud branco combina a profundidade oriental com uma leveza floral surpreendente. Ideal para quem descobre o oud.",
    notes: {
      topo: "Oud Branco, Bergamota",
      meio: "Jasmim, Flor de Laranjeira, Íris",
      base: "Almíscar Branco, Sândalo"
    },
    tags: ["oud", "fresco", "unissexo"]
  },
  {
    id: "rose-taif-pure",
    name: "Rose de Taif Pure",
    category: "rose",
    volume: "3ml",
    price: 110,
    oldPrice: null,
    badge: "Exclusivo",
    icon: "✿",
    shortNotes: "Rosa Pura · Oud · Mel",
    description: "Óleo puro de rosa de Taif, sem qualquer adulteração. Um dos ingredientes mais caros da perfumaria mundial, agora acessível. Uma única gota basta para transformar o seu dia inteiro.",
    notes: {
      topo: "Rosa de Taif Pura",
      meio: "Mel, Cera de Abelha",
      base: "Oud, Âmbar Rosa"
    },
    tags: ["rose", "floral", "feminino"]
  },
  {
    id: "oud-malaki",
    name: "Oud Malaki",
    category: "oud",
    volume: "6ml",
    price: 78,
    oldPrice: null,
    badge: null,
    icon: "♦",
    shortNotes: "Oud Real · Sândalo · Âmbar",
    description: "Uma composição digna da realeza árabe. Oud selvagem da Índia mesclado com sândalo de Mysore e âmbar cinza. Uma fragrância de cerimónia que deixa uma impressão duradoura em todas as ocasiões formais.",
    notes: {
      topo: "Oud Indiano, Açafrão",
      meio: "Sândalo de Mysore, Vetiver",
      base: "Âmbar Cinza, Couro, Musgo"
    },
    tags: ["oud", "formal", "unissexo"]
  },
  {
    id: "mabkhara-set",
    name: "Set Mabkhara + Bakhoor",
    category: "bakhoor",
    volume: "Kit completo",
    price: 58,
    oldPrice: 75,
    badge: "Oferta",
    icon: "⬡",
    shortNotes: "Queimador cerâmico + 100g bakhoor",
    description: "O kit perfeito para quem quer começar a experiência do bakhoor árabe. Inclui uma mabkhara cerâmica artesanal e 100g do nosso bakhoor premium. Uma prenda luxuosa ou o começo de um ritual diário.",
    notes: {
      topo: "Oud, Especiarias Orientais",
      meio: "Âmbar, Rosa",
      base: "Sândalo, Resinas Naturais"
    },
    tags: ["bakhoor", "kit", "oferta"]
  }
];

// Make globally available
window.PRODUCTS = PRODUCTS;
