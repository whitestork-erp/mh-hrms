<template>
	<div class="px-12 py-8 space-y-8">
		<div class="flex items-center">
			<FeatherIcon name="calendar" class="h-7 w-7 text-gray-500 mr-2.5" />
			<span class="font-semibold text-2xl text-gray-500 mr-2">Roster:</span>
			<span class="font-semibold text-2xl">Month View</span>
			<div class="ml-auto space-x-2.5">
				<Dropdown
					:options="VIEW_OPTIONS"
					:button="{
						label: 'View',
						iconRight: 'chevron-down',
						size: 'md',
					}"
				>
				</Dropdown>
				<Dropdown
					:options="[
						{
							label: 'Shift Assignment',
							onClick: () => {
								showShiftAssignmentDialog = true;
							},
						},
					]"
					:button="{
						label: 'Create',
						variant: 'solid',
						iconRight: 'chevron-down',
						size: 'md',
					}"
				/>
			</div>
		</div>
		<MonthViewHeader
			:firstOfMonth="firstOfMonth"
			@updateFilters="updateFilters"
			@addToMonth="addToMonth"
		/>
		<MonthViewTable
			v-if="isCompanySelected"
			ref="monthViewTable"
			:firstOfMonth="firstOfMonth"
			:employees="employees.data || []"
			:employeeFilters="employeeFilters"
			:shiftFilters="shiftFilters"
			:fiscalPeriodDates="fiscalPeriodDates"
		/>
		<div v-else class="py-40 text-center">Please select a company.</div>
	</div>
	<ShiftAssignmentDialog
		v-model="showShiftAssignmentDialog"
		:isDialogOpen="showShiftAssignmentDialog"
		:employees="employees.data"
		@fetchEvents="
			monthViewTable?.events.fetch();
			showShiftAssignmentDialog = false;
		"
	/>
</template>

<script setup lang="ts">
import { ref, reactive, computed, watch } from "vue";
import { Dropdown, FeatherIcon, createListResource } from "frappe-ui";

import { dayjs, goTo, raiseToast } from "../utils";
import MonthViewTable from "../components/MonthViewTable.vue";
import MonthViewHeader from "../components/MonthViewHeader.vue";
import ShiftAssignmentDialog from "../components/ShiftAssignmentDialog.vue";

export type EmployeeFilters = {
	[K in "status" | "company" | "department" | "branch" | "designation"]?: string;
};
export type ShiftFilters = {
	[K in "shift_type" | "shift_location"]?: string;
};

const monthViewTable = ref<InstanceType<typeof MonthViewTable>>();
const isCompanySelected = ref(false);
const showShiftAssignmentDialog = ref(false);
const currentMonth = ref(dayjs().date(1).startOf("D"));
const fiscalPeriodDates = ref<{ month_start: string; month_end: string } | null>(null);

// Computed property that returns the appropriate "first of month" date
// If fiscal period is available, use the fiscal period start date
// Otherwise, use the standard first of month
const firstOfMonth = computed(() => {
	if (fiscalPeriodDates.value) {
		return dayjs(fiscalPeriodDates.value.month_start);
	}
	return currentMonth.value;
});

const employeeFilters = reactive<EmployeeFilters>({
	status: "Active",
});
const shiftFilters = reactive<ShiftFilters>({});

const VIEW_OPTIONS = [
	"Shift Type",
	"Shift Location",
	"Shift Assignment",
	"Shift Schedule",
	"Shift Schedule Assignment",
].map((label) => ({
	label,
	onClick: () => goTo(`/app/${label.toLowerCase().split(" ").join("-")}`),
}));

const addToMonth = (change: number) => {
	currentMonth.value = currentMonth.value.add(change, "M");
	fetchFiscalPeriodDates();
};

const fetchFiscalPeriodDates = async () => {
	if (!employeeFilters.company) {
		fiscalPeriodDates.value = null;
		return;
	}

	try {
		const response = await fetch('/api/method/hrms.api.roster.get_fiscal_period_dates', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				'X-Frappe-CSRF-Token': (window as any).csrf_token
			},
			body: JSON.stringify({
				month_start: currentMonth.value.format("YYYY-MM-DD"),
				company: employeeFilters.company
			})
		});
		const data = await response.json();
		if (data.message) {
			fiscalPeriodDates.value = data.message;
		}
	} catch (error) {
		console.error('Failed to fetch fiscal period dates:', error);
		fiscalPeriodDates.value = null;
	}
};

const updateFilters = async (newFilters: EmployeeFilters & ShiftFilters) => {
	isCompanySelected.value = !!newFilters.company;
	if (!isCompanySelected.value) {
		fiscalPeriodDates.value = null;
		return;
	}

	let employeeUpdated = false;
	(Object.entries(newFilters) as [keyof EmployeeFilters | keyof ShiftFilters, string][]).forEach(
		([key, value]) => {
			if (["shift_type", "shift_location"].includes(key)) {
				if (value) shiftFilters[key] = value;
				else delete shiftFilters[key];
				return;
			}

			if (value) employeeFilters[key] = value;
			else delete employeeFilters[key];
			employeeUpdated = true;
		},
	);

	if (employeeUpdated) {
		await fetchFiscalPeriodDates();
		employees.fetch();
	}
};

// RESOURCES

const employees = createListResource({
	doctype: "Employee",
	fields: ["name", "employee_name", "designation", "image"],
	filters: employeeFilters,
	pageLength: 99999,
	onError(error: { messages: string[] }) {
		raiseToast("error", error.messages[0]);
	},
});
</script>
