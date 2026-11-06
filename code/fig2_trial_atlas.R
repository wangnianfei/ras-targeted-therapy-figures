#!/usr/bin/env Rscript
# ---------------------------------------------------------------------------
# Figure 12 | An atlas of 1,182 RAS-related oncology trials, 2000-2026
#
#   a  world map of trials with at least one registered site
#   b  circular atlas, one sector per trial, grouped by tumour block, with four
#      concentric annotation tracks (relation to RAS, phase, sponsor, status)
#   c  annual registrations by relation to RAS
#
# Layout: A4 text block, 170 mm wide.  Panels are rendered at their final size,
# trimmed to their ink, then placed on fixed rules (left 0, right 170 mm) with
# a single 5 mm gutter between rows.
#
# Inputs
#   <root>/数据/表1_临床试验总表.csv            record-level trial table
#   <root>/figures/FigurePanel_a_world_map.png  panel a, from 03_figures_country.R
# Outputs
#   <root>/figures/Figure_RAS_trial_atlas.pdf / .png / .svg
#
# Usage: Rscript 04_figure_trial_atlas.R <root>
# ---------------------------------------------------------------------------

suppressPackageStartupMessages({
  library(readr); library(dplyr); library(tidyr); library(stringr)
  library(ggplot2); library(scales); library(cowplot); library(png); library(grid)
})

root <- commandArgs(trailingOnly = TRUE)[1]
if (is.na(root)) root <- "."
if (!dir.exists(file.path(root, "数据")))
  stop("run from the project root or pass it as the first argument")
DATA <- file.path(root, "数据"); FIG <- file.path(root, "figures")
mm <- function(x) x / 25.4

# ---- house style -----------------------------------------------------------
FS <- 8; INK <- "#1A1A1A"
sp <- function(x) x / .pt                       # geom_text takes mm, not points
PAL <- c(
  "RAS-targeted" = "#1F3A5F", "RAS-regulator" = "#A63A2E",
  "Biomarker-selected" = "#2A6F6F", "RAS-mentioned" = "#C9A227",
  "ePh1" = "#E0E3E9", "Ph1" = "#B3BCC9", "Ph2" = "#79899F", "Ph3" = "#1F3A5F",
  "Industry" = "#D8D3CB", "Other" = "#B9B3A8", "NIH" = "#9A9488",
  "Network" = "#7B7569", "Gov" = "#5C574D",
  "Completed" = "#F4E7E6", "Ongoing" = "#E4C4C0", "Not yet recruiting" = "#D19992",
  "Stopped early" = "#A63A2E", "Other/unknown" = "#6E241C")

# ---- data ------------------------------------------------------------------
d <- read_csv(file.path(DATA, "表1_临床试验总表.csv"), show_col_types = FALSE)

tumour_block <- function(x) {
  parts <- str_split(str_trim(x), ";")[[1]]
  if (length(parts) > 1) return("Multi-tumour")
  switch(parts,
    "Colorectal cancer" = "Colorectal",
    "Non-small cell lung cancer" = "NSCLC",
    "Pancreatic cancer" = "Pancreatic",
    "Haematologic malignancy" = "Haematologic",
    "Other / unspecified" = "Other",
    if (grepl("histology-agnostic", parts)) "Histology-agnostic" else "Other")
}

d2 <- d %>%
  mutate(
    tumour = sapply(tumour_group, tumour_block),
    year   = as.integer(first_posted_year),
    tier = factor(recode(ras_tier,
      "RAS-targeted"              = "RAS-targeted",
      "RAS-regulator-targeted"    = "RAS-regulator",
      "RAS-biomarker-selected"    = "Biomarker-selected",
      "RAS-mentioned"             = "RAS-mentioned"),
      levels = c("RAS-targeted", "RAS-regulator", "Biomarker-selected", "RAS-mentioned")),
    phase = factor(recode(phase_group,
      "Early Phase 1" = "ePh1", "Phase 1" = "Ph1", "Phase 2" = "Ph2", "Phase 3" = "Ph3"),
      levels = c("ePh1", "Ph1", "Ph2", "Ph3")),
    sponsor = factor(recode(lead_sponsor_class,
      "INDUSTRY" = "Industry", "OTHER" = "Other", "NIH" = "NIH",
      "NETWORK" = "Network", "OTHER_GOV" = "Gov"),
      levels = c("Industry", "Other", "NIH", "Network", "Gov")),
    status = factor(coalesce(status_group, "Other/unknown"),
      levels = c("Completed", "Ongoing", "Not yet recruiting", "Stopped early", "Other/unknown")))

# every trial must land in exactly one level of every track, or the ring would
# silently drop sectors (this happened once with a 4-level status factor)
stopifnot(!any(is.na(d2[, c("tier", "phase", "sponsor", "status", "year")])))

# ---- panel b: sectors ------------------------------------------------------
tumour_order <- d2 %>% count(tumour, sort = TRUE) %>% pull(tumour)
d2 <- d2 %>%
  mutate(tumour = factor(tumour, levels = tumour_order)) %>%
  arrange(tumour, tier, phase, year) %>%
  group_by(tumour) %>% mutate(within = row_number()) %>% ungroup()

GAP_UNITS <- 16                                  # blank arc between blocks
blocks <- d2 %>% group_by(tumour) %>% summarise(n = n(), .groups = "drop") %>%
  mutate(start = cumsum(lag(n + GAP_UNITS, default = 0)) + 1,
         mid   = start + (n - 1) / 2)
d2 <- d2 %>% left_join(blocks %>% select(tumour, start), by = "tumour") %>%
  mutate(x = start + within - 1)

tracks <- tribble(~var, ~ymin, ~ymax,
                  "tier", 3.35, 4.60, "phase", 2.60, 3.18,
                  "sponsor", 1.80, 2.43, "status", 1.00, 1.63)
long <- d2 %>% select(x, tumour, tier, phase, sponsor, status) %>%
  pivot_longer(-c(x, tumour), names_to = "var", values_to = "cat") %>%
  left_join(tracks, by = "var") %>%
  mutate(var = factor(var, levels = c("tier", "phase", "sponsor", "status")))
total_x <- max(d2$x) + GAP_UNITS

ring_plot <- function() {
  ggplot(long) +
    geom_rect(aes(xmin = x - 0.5, xmax = x + 0.5, ymin = ymin, ymax = ymax, fill = cat),
              colour = NA) +
    geom_text(data = blocks, aes(x = mid, y = 5.12, label = paste0(tumour, "\n", n)),
              size = sp(FS), lineheight = .88, colour = INK, family = "Arial") +
    coord_polar(theta = "x", start = 0, direction = -1, clip = "off") +
    scale_fill_manual(values = PAL, guide = "none") +
    scale_x_continuous(limits = c(0.5, total_x), expand = c(0, 0)) +
    scale_y_continuous(limits = c(0, 6.0), expand = c(0, 0)) +
    theme_void() + theme(plot.margin = margin(0, 0, 0, 0))
}

# ---- legend: 2 x 2 key -----------------------------------------------------
levels_by_track <- list(tier = levels(d2$tier), phase = levels(d2$phase),
                        sponsor = levels(d2$sponsor), status = levels(d2$status))
keyd <- long %>% distinct(var, cat) %>% mutate(vk = as.character(var)) %>%
  mutate(ord = mapply(function(v, c) match(c, levels_by_track[[v]]), vk, cat),
         var = factor(vk, levels = c("tier", "phase", "sponsor", "status"),
                      labels = c("RAS relation", "Phase", "Sponsor", "Status"))) %>%
  group_by(var) %>% arrange(ord, .by_group = TRUE) %>% mutate(pos = row_number()) %>% ungroup()

key_plot <- function() {
  ggplot(keyd, aes(x = 1, y = -pos)) +
    geom_tile(aes(fill = cat), width = .36, height = .66, colour = "grey40", linewidth = .12) +
    geom_text(aes(x = 1.26, label = cat), hjust = 0, size = sp(7.2), family = "Arial", colour = INK) +
    facet_wrap(~var, ncol = 2, scales = "free_y") +
    scale_fill_manual(values = PAL, guide = "none") +
    scale_x_continuous(limits = c(0.7, 3.1)) +
    theme_void() +
    theme(strip.text = element_text(size = FS, hjust = 0, face = "bold", family = "Arial",
                                    colour = INK, margin = margin(0, 0, 1.2, 0)),
          panel.spacing.x = unit(2, "mm"), panel.spacing.y = unit(7, "mm"),
          plot.margin = margin(0, 0, 0, 0))
}

# ---- panel c: annual registrations ----------------------------------------
by_year <- d2 %>% count(year, tier) %>%
  complete(year = 2000:2026, tier, fill = list(n = 0))
last_year <- max(d2$year)

timeline_plot <- function() {
  ggplot(by_year, aes(year, n, fill = tier)) +
    geom_area(colour = "white", linewidth = .3) +
    annotate("segment", x = last_year + 0.5, xend = last_year + 0.5, y = 0, yend = 120,
             linetype = "22", linewidth = .3, colour = "grey35") +
    annotate("text", x = last_year - 0.1, y = 127, label = "2026 to 20 Oct", hjust = 1,
             size = sp(7.2), family = "Arial", colour = INK) +
    scale_fill_manual(values = PAL, guide = "none") +
    scale_x_continuous(breaks = seq(2000, 2025, 5), expand = c(0.008, 0.022)) +
    scale_y_continuous(expand = c(0, 0), breaks = c(0, 50, 100), limits = c(0, 140)) +
    labs(x = "Year first posted", y = "Trials per year") +
    theme_classic(base_size = FS) +
    theme(text = element_text(family = "Arial", size = FS, colour = INK),
          axis.line = element_line(linewidth = .3, colour = INK),
          axis.ticks = element_line(linewidth = .3, colour = INK),
          axis.ticks.length = unit(1, "mm"), axis.title = element_text(size = FS),
          axis.text = element_text(size = 7), plot.margin = margin(1, 3, 1, 1))
}

# ---- render at final size, trim to ink ------------------------------------
tmp <- tempfile("fig12_"); dir.create(tmp)
save_png <- function(p, f, w, h)
  ggsave(file.path(tmp, f), p, width = w, height = h, units = "mm", dpi = 600,
         bg = "white", type = "cairo")

save_png(ring_plot(),  "ring.png", 136, 136)
save_png(key_plot(),   "key.png",   68,  78)
save_png(timeline_plot(), "line.png", 170, 40)
if (!file.exists(file.path(FIG, "FigurePanel_a_world_map.png")))
  stop("panel a missing: run 脚本/03_figures_country.R first")
map <- png::readPNG(file.path(FIG, "FigurePanel_a_world_map.png"))

trim <- function(f, pad) {
  img <- png::readPNG(file.path(tmp, f)); if (length(dim(img)) == 2) img <- array(img, c(dim(img), 3))
  ink <- apply(img[, , 1:3], c(1, 2), function(v) any(v < 0.97))
  r <- range(which(apply(ink, 1, any))); c_ <- range(which(apply(ink, 2, any)))
  keep <- img[r[1]:r[2], c_[1]:c_[2], , drop = FALSE]
  list(img = keep, w = (c_[2] - c_[1] + 1) / (600 / 25.4) + 2 * pad,
       h = (r[2] - r[1] + 1) / (600 / 25.4) + 2 * pad)
}
RG <- trim("ring.png", 2.2); KG <- trim("key.png", 2.6)

# ---- assemble on a 170 mm grid -------------------------------------------
W <- 170; GUT <- 5; LINE_H <- 40
MAP_H <- W * dim(map)[1] / dim(map)[2]
ROW2  <- RG$h
H     <- MAP_H + GUT + ROW2 + GUT + LINE_H
y_line <- 0; y_row2 <- LINE_H + GUT; y_map <- y_row2 + ROW2 + GUT
y_key  <- y_row2 + (ROW2 - KG$h) / 2

fig <- ggdraw() +
  draw_grob(rasterGrob(map),    x = 0, y = y_map / H,  width = 1, height = MAP_H / H) +
  draw_grob(rasterGrob(RG$img), x = 0, y = y_row2 / H, width = RG$w / W, height = RG$h / H) +
  draw_grob(rasterGrob(KG$img), x = (W - KG$w) / W, y = y_key / H,
            width = KG$w / W, height = KG$h / H) +
  draw_grob(rasterGrob(trim("line.png", 0)$img), x = 0, y = 0, width = 1, height = LINE_H / H) +
  draw_plot_label(c("a", "b", "c"), c(0.004, 0.004, 0.004),
                  c(1 - 0.004, y_map / H - 0.006, y_row2 / H - 0.006),
                  size = 10, fontface = "bold", family = "Arial")

devices <- if (requireNamespace("svglite", quietly = TRUE)) c("pdf", "svg", "png") else c("pdf", "png")
for (dev in devices) {
  f <- file.path(FIG, paste0("Figure_RAS_trial_atlas.", dev))
  if (dev == "pdf") ggsave(f, fig, width = W, height = H, units = "mm", bg = "white", device = cairo_pdf)
  if (dev == "svg") ggsave(f, fig, width = W, height = H, units = "mm", bg = "white", device = svglite::svglite)
  if (dev == "png") ggsave(f, fig, width = W, height = H, units = "mm", dpi = 600, bg = "white", type = "cairo")
  cat(sprintf("  -> %-46s %3.0f x %3.1f mm\n", basename(f), W, H))
}
unlink(tmp, recursive = TRUE)

# ---- checks quoted in the legend -----------------------------------------
cat("\nfigure-level checks\n")
cat("  trials                        :", nrow(d2), "\n")
cat("  sectors drawn                 :", nrow(long) / 4, "\n")
cat("  blocks (tumour groups)        :", nrow(blocks), "\n")
cat("  block sizes                   :",
    paste(sprintf("%s %d", blocks$tumour, blocks$n), collapse = "; "), "\n")
cat("  RAS relation                  :",
    paste(sprintf("%s %d", names(table(d2$tier)), table(d2$tier)), collapse = "; "), "\n")
cat("  status                        :",
    paste(sprintf("%s %d", names(table(d2$status)), table(d2$status)), collapse = "; "), "\n")
cat("  canvas                        :", sprintf("%.1f x %.1f mm", W, H), "\n")
