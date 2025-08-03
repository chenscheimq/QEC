import matplotlib.pyplot as plt
from PIL import Image

img1 = Image.open('3qubit_e_gap.png')
img2 = Image.open('3qubit_supp.png')
img3 = Image.open('3qubit_corr.png')

# Create a figure
fig = plt.figure(figsize=(10, 10))  # Adjust size as you like

# Define the layout
gs = fig.add_gridspec(2, 2, height_ratios=[1, 1.2])  # more height for img3

# Upper left (img1)
ax1 = fig.add_subplot(gs[0, 0])
ax1.imshow(img1)
ax1.axis('off')

# Upper right (img2)
ax2 = fig.add_subplot(gs[0, 1])
ax2.imshow(img2)
ax2.axis('off')

# Bottom (img3 spans two columns)
ax3 = fig.add_subplot(gs[1, :])
ax3.imshow(img3)
ax3.axis('off')

# Remove almost all spaces
plt.subplots_adjust(
    left=0,    # very close to left
    right=1,   # very close to right
    top=1,     # very close to top
    bottom=0,  # very close to bottom
    wspace=0,  # horizontal space between img1 and img2
    hspace=0   # vertical space between rows
)

plt.tight_layout()
plt.show()
# plt.savefig('together.png',dpi=300)
